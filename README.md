# Project FADAIG: For Absolutely Destroying An iMessage Game

> a.k.a. The Word Hunt Bot

There's actually much more potential for this than just a word hunt bot. The code published here is published in case anyone would find it useful for their own projects. See [here](#license) for license.

## Screenshots

![IMG_3713](https://github.com/ThatXliner/FADAIG/assets/66848002/11ae2f46-8961-4734-bd4d-dfa30b24c3cf)

(screen recording of the bot in action coming soon)


## Parts required

**Host device:** A computer that can run the Python code that sends instructions to the Arduino connected to the target device

**Target device:** An iPad/iPhone that can run GamePidgeon

- [Arduino Leonardo](https://docs.arduino.cc/hardware/leonardo)
- [Serial-to-USB](https://www.amazon.com/dp/B07BBPX8B8)
- [Jumper wires](https://amazon.com/dp/B01EV70C78)
- A micro-USB to USB cable/adapter for connecting the Arduino Leonardo's factory USB port to your target device

## Usage

1. [Install the `src/worker` code](https://github.com/ThatXliner/FADAIG/tree/main/src/worker) onto the Arduino Leonardo
2. [Install the `src/controller` code](https://github.com/ThatXliner/FADAIG/tree/main/src/controller) onto the host device
3. Connect the Arduino Leonardo's factory USB to the target device
4. Connect the serial-to-usb cable
   - Connect the respective `RX`, `TX`, and `GND` pins (`RX`->`TXD`, `TX`->`RXD`, `GND`->`GND`)
   - Connect the other end of the serial-to-usb to the host device
5. Run the `src/controller` code on the host device
   1. Start running the code on the host device
   2. Wait for the program to load the word list
   3. Press "start" on target device
   4. Input the 4x4 board
   5. Profit

## License

Copyright © 2023, Bryan Hu

This project is licensed under the [GNU GPL v3+](https://github.com/ThatXliner/fadaig/blob/main/LICENSE.txt).

In short, this means you can do anything with it (distribute, modify, sell) but if you were to publish your changes, you must make the source code and build instructions readily available.

If you are a company using this project and want an exception, email me at [bryan.hu.2020@gmail.com](mailto:bryan.hu.2020@gmail.com) and we can discuss.
