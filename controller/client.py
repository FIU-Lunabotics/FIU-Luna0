#!/usr/bin/env python3
import socket
import struct
import time
import server
from server import EventCodes


def react_to_event(event_type: int, code: int, value: int):
    if event_type == EventCodes.EVENT_TYPE_BUTTON:
        if value == EventCodes.VALUE_BUTTON_DOWN:
            print(f"button pressed: {code}")
        else:
            print(f"button released: {code}")

    if event_type == EventCodes.EVENT_TYPE_JOYSTICK:
        if code == EventCodes.CODE_LEFT_JOY_HORI:
            print(f"moved left joystick horizontally: {value}")
        if code == EventCodes.CODE_LEFT_JOY_VERT:
            print(f"moved left joystick vertically: {value}")

        if code == EventCodes.CODE_RIGHT_JOY_HORI:
            print(f"moved right joystick horizontally: {value}")
        if code == EventCodes.CODE_RIGHT_JOY_VERT:
            print(f"moved right joystick vertically: {value}")

        if code == EventCodes.CODE_DPAD_HORI:
            print(f"moved dpad horizontally: {value}")
        if code == EventCodes.CODE_DPAD_VERT:
            print(f"moved dpad vertically: {value}")


def connect_to_server(client_socket: socket.socket, hostname: str, port: int):
    """
    Only returns when connection is lost. And therefore should be retried.
    """
    client_socket.connect((hostname, port))
    print("\nConnected succesfully.")

    while True:
        event = client_socket.recv(struct.calcsize(server.EVENT_FORMAT))
        if len(event) == 0:  # did not receive any data, server prob closed
            break

        # first two fields are time in seconds, then time in micro seconds
        (_, _, event_type, code, value) = struct.unpack(server.EVENT_FORMAT, event)
        react_to_event(event_type, code, value)


if __name__ == "__main__":
    print(f"Connecting to {server.HOSTNAME}:{server.PORT} (Press Ctrl+C to stop.)")
    try:
        while True:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                connect_to_server(client_socket, server.HOSTNAME, server.PORT)
                print("Oops! Connection lost.")
                client_socket.shutdown(socket.SHUT_RDWR)
            except ConnectionRefusedError:
                print("Oops, connection was refused, is the server up?")
            except ConnectionResetError:
                print("Oops, connection reset, did server restart? Trying again.")
            finally:
                client_socket.close()
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nFinished gracefully.")
