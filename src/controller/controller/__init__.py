import serial

TTL_TO_USB_PORT = "/dev/tty.usbserial-B0006KP1"


def _send(msg: bytes) -> None:
    with serial.Serial(TTL_TO_USB_PORT) as ser:
        ser.write(msg)
        ser.flush()  # Just in case
        e = ser.readline().strip()
        if e != b"OK":
            msg = "Something is not OK"
            raise RuntimeError(msg)


def absolute_move(x: int, y: int, home: bool = False) -> None:
    _send(f"{'C' if home else 'A'}{x} {y}\n".encode("ascii"))


def home() -> None:
    _send(b"H\n")


# We can only move in increments of 127
# This is a limitation of the USB HID specification
# Where the movement amount is stored as a signed 8
# bit number (2^7 - 1)
INCREMENT = 127  # Maximum value: 127
MAX_INCREMENT = 127


def _gi(n: int, increment: int) -> None:
    if n == 0:
        return n
    if n > 0:
        return increment
    return -increment


def move(x: int, y: int, increment: int = INCREMENT) -> None:
    if increment > MAX_INCREMENT:
        msg = "increment must be between 1 and 127 (inclusive)"
        raise ValueError(msg)
    amount = min(abs(x) // increment, abs(y) // increment)
    for _ in range(amount):
        _send(f"M{_gi(x, increment)} {_gi(y, increment)}\n".encode("ascii"))

    x -= amount * _gi(x, increment)
    y -= amount * _gi(y, increment)

    if abs(x) >= increment:
        amount = abs(x) // increment

        for _ in range(amount):
            _send(f"M{_gi(x, increment)} 0\n".encode("ascii"))
        x -= amount * _gi(x, increment)
    if abs(y) >= increment:
        amount = abs(y) // increment

        for _ in range(amount):
            _send(f"M0 {_gi(y, increment)}\n".encode("ascii"))
        y -= amount * _gi(y, increment)

    _send(
        f"M{(abs(x)%increment) * _gi(x, 1)} {(abs(y)%increment) * _gi(y, 1)}\n".encode(
            "ascii",
        ),
    )


def press() -> None:
    _send(b"P")


def release() -> None:
    _send(b"R")
