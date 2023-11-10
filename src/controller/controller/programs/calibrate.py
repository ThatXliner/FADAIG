from controller import home, release


def calibrate():
    release()
    home()
    while True:
        x, y = list(map(int, input("X, Y: ").split()))
