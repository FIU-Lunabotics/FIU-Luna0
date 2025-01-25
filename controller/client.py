#!/usr/bin/env python3
import pickle
import socket
import time

import server
from evdev import events
import util


def react_to_event(event_type: int, code: int, value: int):
    if event_type == events.EV_KEY:
        action = "pressed" if value == 1 else "released"

        if util.button_north(code):
            print(f"{action} north button")
        elif util.button_east(code):
            print(f"{action} east button")
        elif util.button_south(code):
            print(f"{action} south button")
        elif util.button_west(code):
            print(f"{action} west button")
        elif util.button_lbumper(code):
            print(f"{action} left bumper")
        elif util.button_rbumper(code):
            print(f"{action} right bumper")
        elif util.button_ltrigger(code):
            print(f"{action} left trigger")
        elif util.button_rtrigger(code):
            print(f"{action} right trigger")
        elif util.button_select(code):
            print(f"{action} select")
        elif util.button_start(code):
            print(f"{action} start")
    elif event_type == events.EV_ABS:
        dpad_action = "released" if value == 0 else "pressed"

        if util.dpad_x(code):
            print(f"{dpad_action} dpad x {value}")
        elif util.dpad_y(code):
            print(f"{dpad_action} dpad y {value}")
        elif util.joy_left_x(code):
            print(f"moved left joystick x {value}")
        elif util.joy_left_y(code):
            print(f"moved left joystick y {value}")
        elif util.joy_right_x(code):
            print(f"moved right joystick x {value}")
        elif util.joy_right_y(code):
            print(f"moved right joystick y {value}")
    else:
        print("idk bruh")


def connect_to_server(client_socket: socket.socket, hostname: str, port: int):
    """
    Only returns when connection is lost. And therefore should be retried.
    """
    client_socket.connect((hostname, port))
    print("\nConnected succesfully.")

    while True:
        data = client_socket.recv(1024)
        if len(data) == 0:  # did not receive any data, server prob closed
            break

        event_info: list[int] = pickle.loads(data)
        [event_type, code, value] = event_info
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
