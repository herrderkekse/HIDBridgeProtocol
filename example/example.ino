#include <Keyboard.h>
#include <Mouse.h>

#define TYPE_KEYBOARD 0x10
#define TYPE_MOUSE_MOVE 0x20
#define TYPE_MOUSE_CLICK 0x21

#define EXIT_SUCCESS 0
#define EXIT_FAILURE 1

const float KEYBOARD_DURATION_FACTOR = 5.0 / 255.0;    // in s; ~0.0196s
const float MOUSE_CLICK_DURATION_FACTOR = 1.0 / 255.0; // in s; ~4ms (keep it reasonable, though)

struct Packet
{
  uint8_t init;
  uint8_t cmdType;
  uint8_t data1;
  uint8_t data2;
  uint8_t data3;
  uint8_t end;
};

void setup()
{
  Serial1.begin(9600); // TX/RX Serial communication
  Keyboard.begin();
  Mouse.begin();
}

void loop()
{
  if (Serial1.available() >= 6)
  { // Ensure we have enough bytes

    Packet p = capturePacket();
    printPacket(p);

    // Execute based on command type
    if (p.cmdType == TYPE_KEYBOARD)
    { // Keyboard input
      handleKeyPress(p);
    }
    else if (p.cmdType == TYPE_MOUSE_MOVE)
    { // Mouse movement
      handleMouseMove(p);
    }
    else if (p.cmdType == TYPE_MOUSE_CLICK)
    { // Mouse click
      handleMouseClick(p);
    }
  }
}

void printPacket(Packet p)
{
  Serial1.print("packet recieved: {");
  Serial1.print(p.init);
  Serial1.print(", ");
  Serial1.print(p.cmdType);
  Serial1.print(", ");
  Serial1.print(p.data1);
  Serial1.print(", ");
  Serial1.print(p.data2);
  Serial1.print(", ");
  Serial1.print(p.data3);
  Serial1.print(", ");
  Serial1.print(p.end);
  Serial1.println("}");
}

Packet capturePacket()
{

  uint8_t init = Serial1.read(); // Start byte
  if (init != 0x01)
    return; // Start byte check

  uint8_t cmdType = Serial1.read(); // Command type
  uint8_t data1 = Serial1.read();   // Key/mouse data
  uint8_t data2 = Serial1.read();   // Modifier or extra
  uint8_t data3 = Serial1.read();   // Extra parameter
  uint8_t end = Serial1.read();     // Final bit

  if (end != 0xFF)
    return; // End byte check

  return Packet{
      init, cmdType, data1, data2, data3, end};
}

int handleKeyPress(Packet p)
{
  if (p.cmdType != TYPE_KEYBOARD)
    return EXIT_FAILURE; // can't handle non-keyboard commands

  uint8_t mainKey = p.data1;
  uint8_t modifierKey = p.data2;
  uint8_t holdDurationFactor = p.data3;

  if (modifierKey)
    Keyboard.press(modifierKey);
  Keyboard.press(mainKey);

  // press for the apropriate amount of time; note that non-integer ms implicitally get rounded down
  delay(holdDurationFactor ? KEYBOARD_DURATION_FACTOR * holdDurationFactor * 1000 : 50);

  Keyboard.releaseAll();

  return EXIT_SUCCESS;
}

int handleMouseMove(Packet p)
{
  if (p.cmdType != TYPE_MOUSE_MOVE)
    return EXIT_FAILURE; // can't handle non-mouse-move commands

  signed char xMoveAmount = p.data1;
  signed char yMoveAmount = p.data2;
  uint8_t multiplier = p.data3 ? p.data3 : 1;

  for (int i = 0; i < multiplier; i++)
  {
    Mouse.move(xMoveAmount, yMoveAmount, 0);
  }

  return EXIT_SUCCESS;
}

int handleMouseClick(Packet p)
{
  if (p.cmdType != TYPE_MOUSE_CLICK)
    return EXIT_FAILURE; // can't handle non-mouse-move commands

  uint8_t clickType = p.data1;
  uint8_t numberClicks = p.data2 ? p.data2 : 1;
  uint8_t clickInterval = p.data3;

  for (int i = 0; i < numberClicks; i++)
  {

    if (i > 0)
      delay(clickInterval ? MOUSE_CLICK_DURATION_FACTOR * clickInterval * 1000 : 200);

    Mouse.click(clickType);
  }

  return EXIT_SUCCESS;
}
