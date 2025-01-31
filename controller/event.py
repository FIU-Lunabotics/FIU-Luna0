"""
Controller event abstractions
"""

from evdev import ecodes, AbsInfo
from typing import Tuple

# dict keys are gotten from /usr/include/linux/input-event-codes.h


class AxisEvent:
    def __init__(
        self, code: int, value: int, axis_info: list[Tuple[int, AbsInfo]]
    ) -> None:
        normalized: float
        for axis, info in axis_info:
            if axis == code:
                normalized = (value - info.min) / (info.max - info.min)
                break
        else:
            raise IndexError(f"No info available for axis {code}?")

        self._value = (normalized * 2) - 1
        self._code = code

    def value(self) -> float:
        """
        Returns a value from -1.0 to 1.0, 0 being the center.
        """
        return self._value

    def dpad_x(self) -> bool:
        return self._code == ecodes.ecodes["ABS_HAT0X"]

    def dpad_y(self) -> bool:
        return self._code == ecodes.ecodes["ABS_HAT0Y"]

    def joy_left_x(self) -> bool:
        return self._code == ecodes.ecodes["ABS_X"]

    def joy_left_y(self) -> bool:
        return self._code == ecodes.ecodes["ABS_Y"]

    def joy_right_x(self) -> bool:
        return self._code == ecodes.ecodes["ABS_RX"]

    def joy_right_y(self) -> bool:
        return self._code == ecodes.ecodes["ABS_RY"]

    def pressure_ltrigger(self) -> bool:
        return self._code == ecodes.ecodes["ABS_Z"]

    def pressure_rtrigger(self) -> bool:
        return self._code == ecodes.ecodes["ABS_RZ"]


class ButtonEvent:
    def __init__(self, code: int, value: int, y_north: bool = True) -> None:
        """
        y_north: swaps button self._codes x with y, defaults to True
        """
        if y_north:
            if code == ecodes.ecodes["BTN_X"]:
                code = ecodes.ecodes["BTN_Y"]
            elif code == ecodes.ecodes["BTN_Y"]:
                code = ecodes.ecodes["BTN_X"]

        self._code = code
        self._value = value

    def value(self) -> int:
        """
        Returns 0 if button is released, 1 if pressed.
        """
        return self._value

    def button_north(self) -> bool:
        return self._code == ecodes.ecodes["BTN_NORTH"]

    def button_east(self) -> bool:
        return self._code == ecodes.ecodes["BTN_EAST"]

    def button_south(self) -> bool:
        return self._code == ecodes.ecodes["BTN_SOUTH"]

    def button_west(self) -> bool:
        return self._code == ecodes.ecodes["BTN_WEST"]

    def button_lbumper(self) -> bool:
        return self._code == ecodes.ecodes["BTN_TL"]

    def button_rbumper(self) -> bool:
        return self._code == ecodes.ecodes["BTN_TR"]

    def button_ltrigger(self) -> bool:
        return self._code == ecodes.ecodes["BTN_TL2"]

    def button_rtrigger(self) -> bool:
        return self._code == ecodes.ecodes["BTN_TR2"]

    def button_select(self) -> bool:
        return self._code == ecodes.ecodes["BTN_SELECT"]

    def button_start(self) -> bool:
        return self._code == ecodes.ecodes["BTN_START"]
