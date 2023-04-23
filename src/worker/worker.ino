#include <Mouse.h>
#include <MouseTo.h>
enum class Command { Empty,
                     Move,
                     Press,
                     Release,
                     AbsoluteMove,
                     Home,
                     HomedAbsoluteMove };
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
  switch (currentCommand) {
    case Command::Move:
      Mouse.move(inputX, inputY, 0);
      break;
    case Command::Press:
      Mouse.press();
      break;
    case Command::Release:
      Mouse.release();
      break;
    case Command::AbsoluteMove:
    case Command::HomedAbsoluteMove:
      MouseTo.setTarget(inputX, inputY, currentCommand == Command::HomedAbsoluteMove);
      while (MouseTo.move() == false) {};
      break;
    case Command::Home:
      MouseTo.home();
      break;
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
    case 'C':
      currentCommand = Command::HomedAbsoluteMove;
      break;
    case 'H':
      currentCommand = Command::Home;
      break;
  }
  switch (currentCommand) {
    case Command::Move:
    case Command::AbsoluteMove:
    case Command::HomedAbsoluteMove:
      inputX = Serial1.parseInt();
      inputY = Serial1.parseInt();
      break;
  }
  executeCommand();
  currentCommand = Command::Empty;
  inputX = -1;
  inputY = -1;
  Serial1.println("OK");
  Serial1.flush();
}
