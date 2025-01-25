#!/usr/bin/env python3
import pickle
import socket
import sys
import time

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

        event_info: list[int] = pickle.loads(data)
        [event_type, code, value] = event_info
        react_to_event(event_type, code, value)


def print_help():
    print(f"Usage: {sys.argv[0]} [SERVER_IP]:[PORT] [OPTIONS]")
    print()
    print("Options:")
    print("--help       prints this page")


if __name__ == "__main__":
    server_ip = "localhost"
    server_port = util.DEFAULT_PORT
    for arg in sys.argv[1:]:
        if arg == "--help":
            print("Lunabotics controller client script.")
            print()
            print_help()
            exit(1)
        elif not arg.startswith("--"):
            split = arg.split(":")
            server_ip = split[0]
            if len(split) > 1:
                server_port = int(split[1])
        else:
            print(f'Unknown option: "{arg}"')
            print()
            print_help()
            exit(1)

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
            except socket.gaierror as err:
                if err.errno == -2:
                    print(f'Invalid server IP: "{server_ip}"')
                    print_help()
                    break
                else:
                    raise
            finally:
                client_socket.close()
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nFinished gracefully.")
