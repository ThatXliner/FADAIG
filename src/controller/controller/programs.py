import statistics
import time
from pathlib import Path

import pygtrie
from rich import progress
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

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


SCORE_MAP = {3: 100, 4: 400, 5: 800, 6: 1400, 7: 1800, 8: 2200, 9: 2600}
# Dimensions for center of top left tile
# (For iPad Air 10.9")

# TOP_LEFT_X = 560  # noqa: ERA-0001
# TOP_LEFT_Y = 450  # noqa: ERA-0001
# TILE_SIZE = 130  # noqa: ERA-0001
# (For iPad Pro 12.9")
TOP_LEFT_X = 625
TOP_LEFT_Y = 570

TILE_SIZE = 150


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
        score += SCORE_MAP.get(len(path), 2600)
        is_pressed = False
        start = time.time()
        for tile in path:
            absolute_move(
                TOP_LEFT_X + tile.x * TILE_SIZE, TOP_LEFT_Y + tile.y * TILE_SIZE
            )
            if not is_pressed:
                press()
                is_pressed = True
        release()
        movement_times.append(time.time() - start)
        total_words += 1
    average_time_per_word: float = statistics.mean(movement_times)
    elapsed_time = time.time() - start_time
    table = Table(show_header=False)

    table.add_row("Elapsed time", f"[cyan]{elapsed_time:.2f}[/cyan] seconds")
    table.add_row("Expected score", f"[green]{score}[/green]")
    table.add_row("Expected total words", f"[cyan]{total_words}[/cyan] words")
    table.add_row(
        "Average time per word",
        f"[cyan]{average_time_per_word:.4f}[/cyan] ±"
        f" [cyan]{max(movement_times)-average_time_per_word:.4f}[/cyan] seconds",
    )
    console.print(table)
