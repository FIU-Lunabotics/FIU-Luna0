"""
simple controller input abstractions
"""

from evdev import ecodes

# dict keys are gotten from /usr/include/linux/input-event-codes.h

DEFAULT_PORT = 5000


def button_north(code: int) -> bool:
    return code == ecodes.ecodes["BTN_NORTH"] or code == ecodes.ecodes["BTN_BASE2"]


def button_east(code: int) -> bool:
    return code == ecodes.ecodes["BTN_EAST"] or code == ecodes.ecodes["BTN_BASE3"]


def button_south(code: int) -> bool:
    return code == ecodes.ecodes["BTN_SOUTH"] or code == ecodes.ecodes["BTN_BASE4"]


def button_west(code: int) -> bool:
    return code == ecodes.ecodes["BTN_WEST"] or code == ecodes.ecodes["BTN_BASE5"]


def button_lbumper(code: int) -> bool:
    return code == ecodes.ecodes["BTN_TL"]


def button_rbumper(code: int) -> bool:
    return code == ecodes.ecodes["BTN_TR"]


def button_ltrigger(code: int) -> bool:
    return code == ecodes.ecodes["BTN_TL2"]


def button_rtrigger(code: int) -> bool:
    return code == ecodes.ecodes["BTN_TR2"]


def button_select(code: int) -> bool:
    return code == ecodes.ecodes["BTN_SELECT"]


def button_start(code: int) -> bool:
    return code == ecodes.ecodes["BTN_START"]


def dpad_x(code: int) -> bool:
    return code == ecodes.ecodes["ABS_HAT0X"]


def dpad_y(code: int) -> bool:
    return code == ecodes.ecodes["ABS_HAT0Y"]


def joy_left_x(code: int) -> bool:
    return code == ecodes.ecodes["ABS_X"]


def joy_left_y(code: int) -> bool:
    return code == ecodes.ecodes["ABS_Y"]


def joy_right_x(code: int) -> bool:
    # TODO: snakebyte controller uses the Z's for right joystick, but my off-brand
    # sony one at home uses Z's for triggers so maybe make this swappable?
    return code == ecodes.ecodes["ABS_RX"] or code == ecodes.ecodes["ABS_Z"]


def joy_right_y(code: int) -> bool:
    # TODO: snakebyte controller uses the Z's for right joystick, but my off-brand
    # sony one at home uses Z's for triggers so maybe make this swappable?
    return code == ecodes.ecodes["ABS_RY"] or code == ecodes.ecodes["ABS_RZ"]
