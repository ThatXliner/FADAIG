from __future__ import annotations

import statistics
import time
from collections import deque
from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from collections.abc import Iterator


import pygtrie
from rich import progress
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from controller import absolute_move, home, press, release

DX = [0, 1, 1, 1, 0, -1, -1, -1]
DY = [1, 1, 0, -1, -1, -1, 0, 1]


class LetterPoint(NamedTuple):
    x: int
    y: int
    value: str


PointPath = tuple[LetterPoint, ...]


def logic(point_matrix: list[list[str]], trie: pygtrie.CharTrie) -> Iterator[PointPath]:
    """Run the BFS word-finding logic

    Given a matrix of possible points, yield a tuple of points
    representing a new and unique path.
    """
    max_row_length = len(point_matrix[0])
    max_col_length = len(point_matrix)
    # Every point on the matrix
    initial_points = [
        (LetterPoint(x, y, value),)
        for y, row in enumerate(point_matrix)
        for x, value in enumerate(row)
    ]
    queue: deque[PointPath] = deque(initial_points)
    visited: set[str] = set()
    while queue:
        head = queue.popleft()
        if trie.has_key("".join(letter.value for letter in head)):
            yield head
        for i in range(8):
            last_letter = head[-1]
            new_x = last_letter.x + DX[i]
            new_y = last_letter.y + DY[i]

            if 0 <= new_x < max_row_length and 0 <= new_y < max_col_length:
                new_point = LetterPoint(new_x, new_y, point_matrix[new_y][new_x])
                new_head = (*head, new_point)
                newv: str = "".join(point.value for point in new_head)
                if (
                    newv not in visited
                    and new_point not in head
                    and (trie.has_subtrie(newv) or trie.has_key(newv))
                ):
                    visited.add(newv)
                    queue.append(new_head)


def get_words() -> pygtrie.CharTrie:
    output = pygtrie.CharTrie()
    with progress.open(
        str((Path(__file__).parent.parent.parent / "words.txt").resolve()),
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
# :For iPad Air 10.9-inch:
# TOP_LEFT_X = 560 # noqa: ERA001
# TOP_LEFT_Y = 450 # noqa: ERA001
# TILE_SIZE = 130 # noqa: ERA001
# For iPad Pro 12.9-inch, before iPadOS 17:
# TOP_LEFT_X = 625 # noqa: ERA001
# TOP_LEFT_Y = 570 # noqa: ERA001
# TILE_SIZE = 150 # noqa: ERA001
# For iPad Pro 12.9-inch, after iPadOS 17:
TOP_LEFT_X = 553
TOP_LEFT_Y = 730
TILE_SIZE = 92


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
                TOP_LEFT_X + tile.x * TILE_SIZE,
                TOP_LEFT_Y + tile.y * TILE_SIZE,
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
    table.add_row(
        "Average words per second",
        f"[cyan]{(1/average_time_per_word):.4f}[/cyan]",
    )
    console.print(table)
