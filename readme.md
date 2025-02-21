

# **Binary Command Protocol for Arduino Pro Micro HID Device**

This protocol allows you to send keystrokes (including modifier keys like Shift+Delete), mouse movements, and clicks over a serial connection (usually via the TX/RX-pins) to an **Arduino Pro Micro** or similar. The Pro Micro emulates a USB keyboard and mouse based on the data received over **Serial1**. Therefore it is designed to work well with the Arduino **Mouse.h** and **Keyboard.h** libraries. It is lossely based on the **USB HID protocol** in a very scaled back and simplified way, and as such not to be understood as a standard but rather as a platform to adapt to a specific usecase.


## **Protocol Overview**

The communication between the PC (Python) and the Arduino Pro Micro follows a **binary command protocol** where each command is sent as a sequence of bytes. The structure of the packet is as follows:

| Byte    | Purpose                                                                             |
| ------- | ----------------------------------------------------------------------------------- |
| `0x01`  | **Start Byte** - Marks the beginning of a command                                   |
| `TYPE`  | **Command Type** - Defines the action (`0x10` for keypress, `0x20` for mouse, etc.) |
| `DATA1` | **Main Data** - Corresponds to key codes, mouse X movement, etc.                    |
| `DATA2` | **Additional Data** - Can be modifiers (e.g., Shift), mouse Y movement, etc.        |
| `DATA3` | **Extra Data** - For more options (e.g., duration, multiplier, etc.)                |
| `0xFF`  | **End Byte** - Marks the end of the command (for error-checking)                    |



## **Command Types**

The `TYPE` byte specifies the action to be performed. Here are the available command types:

### **1. Keyboard Command (0x10)**
This command sends a single keystroke, optionally with modifier keys (e.g., Shift, Ctrl, etc.).

| Byte    | Purpose                                                            |
| ------- | ------------------------------------------------------------------ |
| `0x10`  | Command type (Keyboard)                                            |
| `DATA1` | Key code (e.g., `0x6E` for n)                                      |
| `DATA2` | Modifier key (e.g., `0x80` for LEFT CTRL)                          |
| `DATA3` | Duration (in 5/255 of a second; expect `0x00` as default for 50ms) |

Example:  
To send **Ctrl + n** (`0x6E` + `0x80`), send the bytes:
```
0x01, 0x10, 0x80, 0x6E, 0x00, 0xFF
```

### **2. Mouse Movement (0x20)**
This command moves the mouse based on X and Y movements.

| Byte    | Purpose                                              |
| ------- | ---------------------------------------------------- |
| `0x20`  | Command type (Mouse movement)                        |
| `DATA1` | X-axis movement (-128 to 127 i.e. as signed byte)    |
| `DATA2` | Y-axis movement (-128 to 127 i.e. as signed byte)    |
| `DATA3` | multiplier (expect `0x00` as default; same as`0x01`) |

Example:  
To move the mouse **right by 20 pixels** and **down by 10 pixels**, send:
```
0x01, 0x20, 0x14, 0x0A, 0x00, 0xFF
```

### **3. Mouse Click (0x21)**
This command simulates a mouse click.

| Byte    | Purpose                                                             |
| ------- | ------------------------------------------------------------------- |
| `0x21`  | Command type (Mouse click)                                          |
| `DATA1` | Click type (1 = left, 2 = right, 3 = middle )                       |
| `DATA2` | Number of clicks (expect `0x00` as defualt; same as`0x01`)          |
| `DATA3` | Interval ( in 1/255 of a second; expect `0x00` as default for 0.2s) |

Example:  
To send a **double left-click**, send:
```
0x01, 0x21, 0x01, 0x02, 0x00, 0xFF
```

---

## **Python Script Example**

Here’s an example Python script that sends commands to the Pro Micro:

```python
# main.py

import serial
import time
from key_codes import *  # human readable HEX defs


SERIAL_PORT = "/dev/ttyUSB0"  # Adjust for your system
ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)
time.sleep(2)  # Wait for Pro Micro to initialize


def send_command(cmd_type, data1, data2=0x00, data3=0x00):
    packet = bytes([0x01, cmd_type, data1 &
                   0xFF, data2 & 0xFF, data3, 0xFF])
    ser.write(packet)


# Double left click
send_command(TYPE_MOUSE_CLICK, MOUSE_LEFT_CLICK, 0x02)

# press Ctrl + n
send_command(TYPE_KEY, ord('n'), KEY_LEFT_CTRL)

# move mouse 254 pixel to the left and 160 down
send_command(TYPE_MOUSE_MOVE, -127, 80, 2)


ser.close()

```



## **Arduino Code Example**

There is a comprehensive Arduino code example that reads the serial data and performs the corresponding actions in this repository. 


## **Usage**

1. **Connect your Arduino Pro Micro to your PC** via a USB-to-Serial adapter (TX/RX pins).
2. **Run the Python script** to send commands over the serial connection.
3. The **Pro Micro** will receive the commands and perform the actions as if it were a keyboard or mouse.


## **Limitations**

1. **Fixed Key Codes**: The key codes supported by the protocol are limited to the ones defined in the HID standard. Custom or non-standard keys may require additional handling or custom mappings.

2. **Limited Mouse Precision**: Mouse movements are limited to 8-bit signed values for X and Y axes (ranging from -127 to 127), times a shared b-bit unsigned multiplier which restricts the precision of movements. Fine-grained control (e.g., less then \< multiplier \> - pixel movements) may not be achievable.

3. **Single Command per Packet**: Each packet can only execute **one action at a time** (one key press, mouse movement, or click). For complex sequences (e.g., typing a string or mouse movements), multiple packets must be sent.

4. **No Feedback Mechanism**: The protocol does not include any built-in feedback to confirm whether a command was successfully executed on the Pro Micro. While the Pro Micro can send a confirmation signal back over Serial1, this isn't implemented in the current protocol (yet it is used informally in the code example).

5. **Limited Modifiers**: The protocol supports only a single modifier key (e.g., Shift, Ctrl) with each key press. Complex combinations (e.g., Ctrl+Shift+Alt) would require sending additional commands or modifying the protocol.

6. **Serial Baud Rate**: The protocol assumes communication over a 9600 baud serial connection. Higher baud rates might be used, but care must be taken to ensure the baud rate is stable and does not cause data loss or timing issues.

7. **No Mouse Scroll or Advanced Features**: Mouse interactions are limited to basic movements and clicks. More advanced mouse features like scrolling or multi-button clicks are not yet supported.



## **Conclusion**

This binary protocol enables compact and efficient communication between your PC and Arduino Pro Micro, allowing for the sending of **keystrokes**, **mouse movements**, and **clicks**, including **modifier keys** like Shift and Ctrl. Feel free to modify to fit your needs and adress some of the limitations!

