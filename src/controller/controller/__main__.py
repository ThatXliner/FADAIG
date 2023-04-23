import readline  # noqa
from pathlib import Path

import pygtrie

from controller import press, release, logic, absolute_move, home


def get_words():
    output = pygtrie.CharTrie()
    for word in (Path(__file__).parent.parent / "words.txt").read_text().splitlines():
        output[word.lower()] = object()
    return output


def autoclicker():
    release()
    is_pressed = False
    while True:
        if is_pressed:
            is_pressed = False
            release()
        else:
            is_pressed = True
            press()


def main():
    release()
    home()
    is_pressed = False
    while True:
        try:
            cmd = input(">").split()
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


def main():
    release()
    print("Loading words")
    words = get_words()
    # Move to top left corner
    absolute_move(0, 0, True)
    input("Ready to go? [press ENTER]")
    tiles = [list(input(">").lower()) for _ in range(4)]
    for path in logic(tiles, words):
        is_pressed = False
        for tile in path:
            # 560, 450 is the top left tile
            absolute_move(560 + tile.x * 130, 450 + tile.y * 130)
            if not is_pressed:
                press()
                is_pressed = True
        release()


if __name__ == "__main__":
    main()
