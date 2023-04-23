from pathlib import Path

import pygtrie

from controller import move, press, release

# Each tile is 160x160 pixels

# My iPad Air (4th gen) is 2360x1640 pixels

# move 901x757 for center of top left tile


# 26 pixels in between each tile


# To move to a tile X tiles to the right of you and Y tiles below you
# (assuming you're current at the center of a tile, coords (A,B))

# 4x4 tiles


# Go to (A+X*186, B+Y*186)
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
        else:
            move(*list(map(int, cmd)))


# def main():
#     release()
#     print("Loading words")
#     words = get_words()
#     # Move to top left corner
#     move(-900, -900)
#     # move(-2360, -1640)
#     input("Ready to go? [press ENTER]")
#     # move = lambda *args: print("MOVED: ", *args)
#     # press = lambda: print("PRESSED")
#     # release = lambda: print("RELEASED")
#     # Move to the center of the top left tile
#     tiles = [list(input(">").lower()) for _ in range(4)]
#     move(300, 255)
#     # move(901, 757)
#     cur_x = 0
#     cur_y = 0
#     for path in logic(tiles, words):
#         is_pressed = False
#         for tile in path:
#             x = tile.x - cur_x
#             y = tile.y - cur_y
#             move(x * 55, y * 55, increment=35)
#             input("[NEXT]")
#             # move(x * 186, y * 186)
#             cur_x, cur_y = tile.x, tile.y
#             if not is_pressed:
#                 press()
#                 is_pressed = True
#         release()


if __name__ == "__main__":
    main()
