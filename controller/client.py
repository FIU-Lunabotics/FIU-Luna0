#!/usr/bin/env python3
import pickle
import socket
import sys
import time

from event import AxisEvent, ButtonEvent
import util


def react_to_event(event: AxisEvent | ButtonEvent):
    if type(event) is AxisEvent:
        dpad_action = "released" if event.value() == 0 else "pressed"

        if event.dpad_x():
            print(f"{dpad_action} dpad x {event.value()}")
        elif event.dpad_y():
            print(f"{dpad_action} dpad y {event.value()}")
        elif event.joy_left_x():
            print(f"moved left joystick x {event.value()}")
        elif event.joy_left_y():
            print(f"moved left joystick y {event.value()}")
        elif event.joy_right_x():
            print(f"moved right joystick x {event.value()}")
        elif event.joy_right_y():
            print(f"moved right joystick y {event.value()}")
    elif type(event) is ButtonEvent:
        action = "pressed" if event._value == 1 else "released"

        if event.button_north():
            print(f"{action} north button")
        elif event.button_east():
            print(f"{action} east button")
        elif event.button_south():
            print(f"{action} south button")
        elif event.button_west():
            print(f"{action} west button")
        elif event.button_lbumper():
            print(f"{action} left bumper")
        elif event.button_rbumper():
            print(f"{action} right bumper")
        elif event.button_ltrigger():
            print(f"{action} left trigger")
        elif event.button_rtrigger():
            print(f"{action} right trigger")
        elif event.button_select():
            print(f"{action} select")
        elif event.button_start():
            print(f"{action} start")
    else:
        print("idk bruh")


def connect_to_server(client_socket: socket.socket, ip: str, port: int):
    """
    Only returns when connection is lost. And therefore should be retried.
    """
    client_socket.connect((ip, port))
    print("\nConnected successfully.")

    while True:
        data = client_socket.recv(1024)
        if len(data) == 0:  # did not receive any data, server prob closed
            break

        print(f"len: {len(data)}")
        event = pickle.loads(data)
        react_to_event(event)


def fatal_help(message: str):
    """
    Prints help with the given message at the top,
    then exits with error status (1)
    """
    print(message)
    print()
    print(f"Usage: {sys.argv[0]} [SERVER_IP]:[PORT] [OPTIONS]")
    print()
    print("Options:")
    print("--help       prints this page")
    exit(1)


if __name__ == "__main__":
    server_ip = "localhost"
    server_port = util.DEFAULT_PORT
    for arg in sys.argv[1:]:
        if arg == "--help":
            fatal_help("Lunabotics controller client script.")
        elif not arg.startswith("--"):
            split = arg.split(":")
            if split[0]:  # only set if ip exists, e.g. ignore for input ":2121"
                server_ip = split[0]
            if len(split) > 1:
                if not split[1].isdigit():
                    fatal_help(f'Port "{split[1]}" is not valid in {arg}')
                server_port = int(split[1])
        else:
            fatal_help(f'Unknown option: "{arg}"')

    print(f"Connecting to {server_ip}:{server_port} (Press Ctrl+C to stop.)")
    try:
        while True:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                connect_to_server(client_socket, server_ip, server_port)
                print("Oops! Connection lost.")
                client_socket.shutdown(socket.SHUT_RDWR)
            except ConnectionRefusedError:
                print("Oops, connection was refused, is the server up?")
            except ConnectionResetError:
                print("Oops, connection reset, did server restart? Trying again.")
            except socket.gaierror:
                fatal_help(f'Invalid server IP: "{server_ip}"')
                break
            finally:
                client_socket.close()
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nFinished gracefully.")
