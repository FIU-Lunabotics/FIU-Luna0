"""
simple controller input abstractions
"""

from evdev import ecodes
import os
import logging

# dict keys are gotten from /usr/include/linux/input-event-codes.h

DEFAULT_PORT = 5000


def init_logger() -> logging.Logger:
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    try:
        log_level = getattr(logging, log_level)
    except AttributeError:
        log_level = logging.INFO

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    handler = logging.StreamHandler()
    handler.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def button_north(code: int) -> bool:
    return code == ecodes.ecodes["BTN_NORTH"]


def button_east(code: int) -> bool:
    return code == ecodes.ecodes["BTN_EAST"]


def button_south(code: int) -> bool:
    return code == ecodes.ecodes["BTN_SOUTH"]


def button_west(code: int) -> bool:
    return code == ecodes.ecodes["BTN_WEST"]


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
    return code == ecodes.ecodes["ABS_RX"]


def joy_right_y(code: int) -> bool:
    return code == ecodes.ecodes["ABS_RY"]


def pressure_ltrigger(code: int) -> bool:
    return code == ecodes.ecodes["ABS_Z"]


def pressure_rtrigger(code: int) -> bool:
    return code == ecodes.ecodes["ABS_RZ"]
