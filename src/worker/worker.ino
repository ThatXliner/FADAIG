#include <Mouse.h>
#include <MouseTo.h>
enum class Command { Empty, Move, Press, Release, AbsoluteMove };
long inputX;
long inputY;
Command currentCommand = Command::Empty;
void setup() {
    Serial1.begin(9600);
    inputX = -1;
    inputY = -1;
    Mouse.begin();
    // TODO: Calibrate correction factor, calibrate actual screen resolution
    MouseTo.setCorrectionFactor(1);
}
void executeCommand() {
    if (currentCommand == Command::Move) {
        Mouse.move(inputX, inputY, 0);
    } else if (currentCommand == Command::Press) {
        Mouse.press();
    } else if (currentCommand == Command::Release) {
        Mouse.release();
    } else if (currentCommand == Command::AbsoluteMove) {
        MouseTo.setTarget(inputX, inputY);
        while (MouseTo.move() == false) {}
    }
}
void loop() {
    while (Serial1.available() == 0) {
    };
    char command = Serial1.read();
    switch (command) {
        case 'M':
            currentCommand = Command::Move;
            break;
        case 'P':
            currentCommand = Command::Press;
            break;
        case 'R':
            currentCommand = Command::Release;
            break;
        case 'A':
            currentCommand = Command::AbsoluteMove;
            break;
    }
    if (currentCommand == Command::Move || currentCommand == Command::AbsoluteMove) {
        inputX = Serial1.parseInt();
        inputY = Serial1.parseInt();
    }
    executeCommand();
    currentCommand = Command::Empty;
    inputX = -1;
    inputY = -1;
    Serial1.println("OK");
    Serial1.flush();
}
