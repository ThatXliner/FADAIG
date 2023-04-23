# Arduino

This folder contains the Arduino code to run on an [Arduino Leonardo](https://docs.arduino.cc/hardware/leonardo), connected to the target device with the [TTL/Serial-to-USB](https://www.amazon.com/dp/B07BBPX8B8) connected to the host computer.

## Dependencies

- [`Mouse.h`](https://www.arduino.cc/reference/en/language/functions/usb/mouse/) - should be built-in with the Arduino Leonardo.
- [`MouseTo.h`](https://github.com/per1234/MouseTo) - see their installation instructions

## Installation

1. Plug the built-in (factory included) usb port (micro USB I believe) on the Leonardo to the host computer (usually via USB cable)
2. Open this directory in the Arduino IDE
3. Upload the `worker.ino` sketch to the Leonardo (see [here](https://stackoverflow.com/a/50006773/15396573) for fixing `avrdude: butterfly_recv(): programmer is not responding`)

After you upload, you should see

```
Connecting to programmer: .
Found programmer: Id = "CATERIN"; type = S
    Software Version = 1.0; No Hardware Version given.
Programmer supports auto addr increment.
Programmer supports buffered memory access with buffersize=128 bytes.

Programmer supports the following devices:
    Device code: 0x44
```

Or something similar
