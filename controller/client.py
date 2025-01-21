#!/usr/bin/env python3
import socket
import struct
from server import EVENT_FORMAT, EventCodes, HOSTNAME, PORT


def react_to_event(event_type, code, value):
    if event_type == EventCodes.EVENT_TYPE_BUTTON:
        print(f"button pressed: {code}")

    if event_type == EventCodes.EVENT_TYPE_JOYSTICK:
        if code == EventCodes.CODE_LEFT_JOY_HORI:
            print(f"moved left joystick horizontally: {value}")
        if code == EventCodes.CODE_LEFT_JOY_VERT:
            print(f"moved left joystick vertically: {value}")

        if code == EventCodes.CODE_RIGHT_JOY_HORI:
            print(f"moved right joystick horizontally: {value}")
        if code == EventCodes.CODE_RIGHT_JOY_VERT:
            print(f"moved right joystick vertically: {value}")


if __name__ == "__main__":
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((HOSTNAME, PORT))

    while True:
        event = clientsocket.recv(struct.calcsize(EVENT_FORMAT))
        # first two fields are time seconds, and time micro seconds
        (_, _, event_type, code, value) = struct.unpack(EVENT_FORMAT, event)
        react_to_event(event_type, code, value)
