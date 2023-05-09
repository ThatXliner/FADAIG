import statistics
import time
from pathlib import Path

import pygtrie
from rich import progress
from rich.console import Console
from rich.prompt import Prompt

from controller import absolute_move, home, logic, press, release


def get_words() -> pygtrie.CharTrie:
    output = pygtrie.CharTrie()
    with progress.open(
        str((Path(__file__).parent.parent / "words.txt").resolve()),
        "r",
        encoding="utf-8",
        description="[blue]Loading word list",
    ) as file:
        for word in file:
            # A unique object to mark the end of the trie
            output[word.lower().rstrip()] = object()
    return output


def auto_clicker() -> None:
    release()
    is_pressed = False
    while True:
        if is_pressed:
            is_pressed = False
            release()
        else:
            is_pressed = True
            press()


def mouse_shell() -> None:
    release()
    home()
    is_pressed = False
    while True:
        try:
            cmd = Prompt.ask(">").split()
        except EOFError:
            break
        if not cmd:
            if is_pressed:
                is_pressed = False
                release()
            else:
                is_pressed = True
                press()
        elif cmd == ["*"]:
            home()
        else:
            homed = False
            if cmd[0] == "*":
                cmd.pop(0)
                homed = True
            absolute_move(*list(map(int, cmd)), homed)


SCORE_MAP = {3: 100, 4: 400, 5: 800, 6: 1400, 7: 1800}


def word_hunt() -> None:
    console = Console()
    release()
    words = get_words()
    # Move to top left corner
    absolute_move(0, 0, home=True)
    tiles = [list(Prompt.ask(">").lower()) for _ in range(4)]

    start_time = time.time()
    score = 0
    total_words = 0
    movement_times = []
    for path in progress.track(
        list(reversed(list(logic(tiles, words)))),
        description="Running bot...",
    ):
        score += SCORE_MAP.get(len(path), 1800)
        is_pressed = False
        start = time.time()
        for tile in path:
            # 560, 450 is the top left tile
            absolute_move(560 + tile.x * 130, 450 + tile.y * 130)
            if not is_pressed:
                press()
                is_pressed = True
        release()
        movement_times.append(time.time() - start)
        total_words += 1
    average_time_per_word: float = statistics.mean(movement_times)
    elapsed_time = time.time() - start_time
    console.print(f"[bold]Elapsed time:[/bold] [cyan]{elapsed_time}[/cyan] seconds")
    console.print(f"[bold]Expected score:[/bold] [green]{score}[/green]")
    console.print(f"[bold]Expected total words:[/bold] {total_words}")
    console.print(
        f"[bold]Average time per word:[/bold] {average_time_per_word} ±"
        f" {max(movement_times)-average_time_per_word}",
    )
