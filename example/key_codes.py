
# Define key codes in human-readable names for easy reference
# For ASCII-keys use pythons built in ord() funktion. I.e. ord('c') for the c-key

# Custom definistions
# Type selectors
TYPE_KEY = 0x10
TYPE_MOUSE_MOVE = 0x20
TYPE_MOUSE_CLICK = 0x21

# Mouse buttons (for click commands)
MOUSE_LEFT_CLICK = 0x01
MOUSE_RIGHT_CLICK = 0x02
MOUSE_MIDDLE_CLICK = 0x04

# Arduino Keyboard.h definitions
# Keyboard modifiers
KEY_LEFT_CTRL = 0x80
KEY_LEFT_SHIFT = 0x81
KEY_LEFT_ALT = 0x82
KEY_LEFT_GUI = 0x83
KEY_RIGHT_CTRL = 0x84
KEY_RIGHT_SHIFT = 0x85
KEY_RIGHT_ALT = 0x86
KEY_RIGHT_GUI = 0x87

# Within the alphanumeric cluster
KEY_TAB = 0xB3
KEY_CAPS_LOCK = 0xC1
KEY_BACKSPACE = 0xB2
KEY_RETURN = 0xB0
KEY_MENU = 0xED

# Navigation cluster
KEY_INSERT = 0xD1
KEY_DELETE = 0xD4
KEY_HOME = 0xD2
KEY_END = 0xD5
KEY_PAGE_UP = 0xD3
KEY_PAGE_DOWN = 0xD6
KEY_UP_ARROW = 0xDA
KEY_DOWN_ARROW = 0xD9
KEY_LEFT_ARROW = 0xD8
KEY_RIGHT_ARROW = 0xD7

# Numeric keypad
KEY_NUM_LOCK = 0xDB
KEY_KP_SLASH = 0xDC
KEY_KP_ASTERISK = 0xDD
KEY_KP_MINUS = 0xDE
KEY_KP_PLUS = 0xDF
KEY_KP_ENTER = 0xE0
KEY_KP_1 = 0xE1
KEY_KP_2 = 0xE2
KEY_KP_3 = 0xE3
KEY_KP_4 = 0xE4
KEY_KP_5 = 0xE5
KEY_KP_6 = 0xE6
KEY_KP_7 = 0xE7
KEY_KP_8 = 0xE8
KEY_KP_9 = 0xE9
KEY_KP_0 = 0xEA
KEY_KP_DOT = 0xEB

# Escape and function keys
KEY_ESC = 0xB1
KEY_F1 = 0xC2
KEY_F2 = 0xC3
KEY_F3 = 0xC4
KEY_F4 = 0xC5
KEY_F5 = 0xC6
KEY_F6 = 0xC7
KEY_F7 = 0xC8
KEY_F8 = 0xC9
KEY_F9 = 0xCA
KEY_F10 = 0xCB
KEY_F11 = 0xCC
KEY_F12 = 0xCD
KEY_F13 = 0xF0
KEY_F14 = 0xF1
KEY_F15 = 0xF2
KEY_F16 = 0xF3
KEY_F17 = 0xF4
KEY_F18 = 0xF5
KEY_F19 = 0xF6
KEY_F20 = 0xF7
KEY_F21 = 0xF8
KEY_F22 = 0xF9
KEY_F23 = 0xFA
KEY_F24 = 0xFB

# Function control keys
KEY_PRINT_SCREEN = 0xCE
KEY_SCROLL_LOCK = 0xCF
KEY_PAUSE = 0xD0
