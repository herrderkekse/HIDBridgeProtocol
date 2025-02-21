
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

    # optionally wait for a response and print it
    time.sleep(0.1)
    response = ser.readline().decode().strip()
    if response:
        print("Arduino Response:", response)


# Double left click
send_command(TYPE_MOUSE_CLICK, MOUSE_LEFT_CLICK, 0x02)

# press Ctrl + n
send_command(TYPE_KEY, ord('n'), KEY_LEFT_CTRL)

# move mouse 254 pixel to the left and 160 down
send_command(TYPE_MOUSE_MOVE, -127, 80, 2)


ser.close()
