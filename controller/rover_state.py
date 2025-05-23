"""class that keeps track of the current state of the Rover"""

import json

from typing import OrderedDict
from event import AxisEvent, ButtonEvent

<<<<<<< HEAD

=======
>>>>>>> Debug
NORTH = "N"
EAST = "E"
SOUTH = "S"
WEST = "W"
JOY_LEFT_X = "LjoyX"
JOY_LEFT_Y = "LjoyY"
JOY_RIGHT_X = "RjoyX"
JOY_RIGHT_Y = "RjoyY"
STICK_LEFT = "LS"
STICK_RIGHT = "RS"
DPAD_X = "dX"
DPAD_Y = "dY"
TRIGGER_LEFT = "LT"
TRIGGER_RIGHT = "RT"
BUMPER_LEFT = "LB"
BUMPER_RIGHT = "RB"
SELECT = "SELECT"
START = "START"

<<<<<<< HEAD
count = 0
=======
>>>>>>> Debug

class RoverState:
    def __init__(self):
        self._tank_mode: bool = False
        self._controller_state: OrderedDict[str, int] = OrderedDict()
        self._controller_state[NORTH] = 0
        self._controller_state[EAST] = 0
        self._controller_state[SOUTH] = 0
        self._controller_state[WEST] = 0
        self._controller_state[STICK_LEFT] = 0
        self._controller_state[STICK_RIGHT] = 0
        self._controller_state[DPAD_X] = 0
        self._controller_state[DPAD_Y] = 0
        self._controller_state[BUMPER_LEFT] = 0
        self._controller_state[BUMPER_RIGHT] = 0
        self._controller_state[JOY_LEFT_X] = 127  # assume joysticks are centered.
        self._controller_state[JOY_LEFT_Y] = 127
        self._controller_state[JOY_RIGHT_X] = 127
        self._controller_state[JOY_RIGHT_Y] = 127
        self._controller_state[TRIGGER_LEFT] = 0
        self._controller_state[TRIGGER_RIGHT] = 0
        self._controller_state[SELECT] = 0
        self._controller_state[START] = 0

    def __str__(self) -> str:
        state = json.dumps(self._controller_state, indent=4)
<<<<<<< HEAD
        # to not trigger issues with the byte order
        
        return f"Controller state: {state}"
    
    def get_binary_data(self) -> bytes:
        """
        Will return a PACKET FOR DEBUG of size 8 in the format:
        [255, bitmask, joy_left_x, joy_left_y, joy_right_x, joy_right_y, 0, 255]
        """
        state = self._controller_state
        
        startByte = 0b10101000
        endByte   = 0b00010101       

        if state[SOUTH]:
            startByte = startByte | 0b00000100
        if state[EAST]:
            startByte = startByte | 0b00000010
        if state[WEST]:
            startByte = startByte | 0b00000001
        if state[NORTH]:
            endByte = endByte | 0b10000000
        if state[BUMPER_RIGHT]:
            endByte = endByte | 0b01000000
        if state[BUMPER_LEFT]:
            endByte = endByte | 0b00100000

        return bytes(
            [ # CHANGE TO MATCH ARDUINO DATA RECIEVES
                startByte,
                state[JOY_LEFT_X],
                state[JOY_LEFT_Y],
                state[JOY_RIGHT_Y],
                state[TRIGGER_RIGHT],
                endByte
            ]
        )
    
=======
        return f"Tank mode: {self._tank_mode}\nController state: {state}"

>>>>>>> Debug
    def get_arduino_data(self) -> bytes:
        """
        Will return a bytes object of size 8 in the format:
        [255, bitmask, joy_left_x, joy_left_y, joy_right_x, joy_right_y, 0, 255]
        """
        state = self._controller_state
<<<<<<< HEAD
        
        startByte = 0b10101000
        endByte   = 0b00010101       

        if state[SOUTH]:
            startByte = startByte | 0b00000100
        if state[EAST]:
            startByte = startByte | 0b00000010
        if state[WEST]:
            startByte = startByte | 0b00000001
        if state[NORTH]:
            endByte = endByte | 0b10000000
        if state[BUMPER_RIGHT]:
            endByte = endByte | 0b01000000
        if state[BUMPER_LEFT]:
            endByte = endByte | 0b00100000

        return bytes(
            [ # CHANGE TO MATCH ARDUINO DATA RECIEVES
                startByte,
                state[JOY_LEFT_X],
                state[JOY_LEFT_Y],
                state[JOY_RIGHT_Y],
                state[TRIGGER_RIGHT],
                endByte
=======
        bitmask = int(self._tank_mode)  # for now
        return bytes(
            [
                255,
                bitmask,
                state[JOY_LEFT_X],
                state[JOY_LEFT_Y],
                state[JOY_RIGHT_X],
                state[JOY_RIGHT_Y],
                0,  # placeholder
                255,
>>>>>>> Debug
            ]
        )

    def take_event(self, event: AxisEvent | ButtonEvent):
        if type(event) is AxisEvent:
            if event.dpad_x():
                self._controller_state[DPAD_X] = event.value()
            elif event.dpad_y():
                self._controller_state[DPAD_Y] = event.value()
            elif event.joy_left_x():
                self._controller_state[JOY_LEFT_X] = event.value()
            elif event.joy_left_y():
                self._controller_state[JOY_LEFT_Y] = event.value()
            elif event.joy_right_x():
                self._controller_state[JOY_RIGHT_X] = event.value()
            elif event.joy_right_y():
                self._controller_state[JOY_RIGHT_Y] = event.value()
            elif event.pressure_ltrigger():
                self._controller_state[TRIGGER_LEFT] = event.value()
            elif event.pressure_rtrigger():
                self._controller_state[TRIGGER_RIGHT] = event.value()
        elif type(event) is ButtonEvent:
            if event.button_north():
                self._controller_state[NORTH] = event.value()
            elif event.button_east():
                self._controller_state[EAST] = event.value()
            elif event.button_south():
                self._controller_state[SOUTH] = event.value()
            elif event.button_west():
                self._controller_state[WEST] = event.value()
            elif event.button_lbumper():
                self._controller_state[BUMPER_LEFT] = event.value()
            elif event.button_rbumper():
                self._controller_state[BUMPER_RIGHT] = event.value()
            elif event.button_ltrigger():
                self._controller_state[TRIGGER_LEFT] = event.value()
            elif event.button_rtrigger():
                self._controller_state[TRIGGER_RIGHT] = event.value()
            elif event.button_lstick():
                self._controller_state[STICK_LEFT] = event.value()
            elif event.button_rstick():
                self._controller_state[STICK_RIGHT] = event.value()
            elif event.button_select():
                self._controller_state[SELECT] = event.value()
            elif event.button_start():
                self._controller_state[START] = event.value()
                self._tank_mode = not self._tank_mode
