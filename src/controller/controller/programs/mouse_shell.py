"""Useful for calibration"""
from rich.prompt import Prompt

from controller import absolute_move, home, press, release


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
