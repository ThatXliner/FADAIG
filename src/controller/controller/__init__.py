from collections import deque
from collections.abc import Iterator
from typing import NamedTuple

import pygtrie
import serial

TTL_TO_USB_PORT = "/dev/tty.usbserial-B0006KP1"


def _send(msg: bytes) -> None:
    print(msg)  # noqa: T201
    with serial.Serial(TTL_TO_USB_PORT) as ser:
        ser.write(msg)
        ser.flush()  # Just in case
        e = ser.readline().strip()
        if e != b"OK":
            msg = "Something is not OK"
            raise RuntimeError(msg)


# We can only go in increments of 127
# This is a limitation of the USB HID specification
# Where the movement amount is stored as a signed 8
# bit number (2^7 - 1)
INCREMENTS = 127  # MAX:127


def _gi(n, increment):
    if n == 0:
        return n
    if n > 0:
        return increment
    return -increment


def move(x: int, y: int, increments=INCREMENTS) -> None:
    # TODO: Verify the math
    for _ in range(min(abs(x // increments), abs(y // increments))):
        _send(f"M{_gi(x)} {_gi(y)}\n".encode("ascii"))
    x -= increments * min(abs(x // increments), abs(y // increments)) * _gi(x, 1)
    y -= increments * min(abs(x // increments), abs(y // increments)) * _gi(y, 1)

    if abs(x) > increments:
        for _ in range(abs(x // increments)):
            _send(f"M{_gi(x)} 0\n".encode("ascii"))
        x -= increments * abs(x // increments) * _gi(x, 1)
    if abs(y) > increments:
        for _ in range(abs(y // increments)):
            _send(f"M0 {_gi(y)}\n".encode("ascii"))
        y -= increments * abs(y // increments) * _gi(y, 1)
    # X % Y where Y > 0 is the same as |X| % Y
    _send(f"M{x%increments} {y%increments}\n".encode("ascii"))


def press() -> None:
    _send("P".encode("ascii"))


def release() -> None:
    _send("R".encode("ascii"))


DX = [0, 1, 1, 1, 0, -1, -1, -1]
DY = [1, 1, 0, -1, -1, -1, 0, 1]


class LetterPoint(NamedTuple):
    x: int
    y: int
    value: str


PointPath = tuple[LetterPoint, ...]


def logic(point_matrix: list[list[str]], trie: pygtrie.CharTrie) -> Iterator[PointPath]:
    """Given a matrix of possible points, yield a tuple
    of points representing a new and unique path."""

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
                    and trie.has_subtrie(newv)
                ):
                    visited.add(newv)
                    queue.append(new_head)
