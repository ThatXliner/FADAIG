from controller import absolute_move, home, logic, press, release


def calibrate():
    release()
    home()
    while True:
        x, y = list(map(int, input("X, Y: ").split()))
