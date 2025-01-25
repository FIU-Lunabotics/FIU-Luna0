#!/usr/bin/env python3
import pickle
import socket
import sys
import time

import evdev
from evdev import events

from util import DEFAULT_PORT


def read_joystick(client_socket: socket.socket):
    controller: evdev.InputDevice
    # select first device with joysticks as controller
    for path in evdev.list_devices():
        device = evdev.InputDevice(path)
        # check if device has axis movement (joysticks)
        if events.EV_ABS in device.capabilities(absinfo=False):
            controller = device
            break
    else:
        raise FileNotFoundError

    print(f"Controller found: {controller.name}")
    for event in controller.read_loop():
        # we do not care about the time of the event, therefore sending this list[int]
        # instead of an InputEvent takes each pickle from ~104 bytes to 22-23 in tests
        data = [event.type, event.code, event.value]
        if sum(data) != 0:  # all-zero events are ignored
            client_socket.sendall(pickle.dumps(data))


def try_handle_client(client_socket: socket.socket):
    first_fail = True
    while True:  # preferred over recursively calling to avoid stack overflow
        try:
            read_joystick(client_socket)
        except FileNotFoundError:
            if first_fail:
                print("Controller not found, connect pls.")
        except BrokenPipeError:
            print("Failed to send controller event, did client disconnect?")
            break
        except OSError as err:
            if err.errno == 19:
                print("Oops! controller no longer exists, did it disconnect?")
            else:
                raise
        finally:
            first_fail = False

        time.sleep(2)


def start_server(server_socket: socket.socket, ip: str, port: int):
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((ip, port))

    # arg is how many connections to queue. more than 1 would mean something has gone wrong tbh
    server_socket.listen(5)

    print(f"Server listening on {ip}:{port}")
    print("Press Ctrl+C to stop.")
    while True:
        client_socket, (client_ip, client_port) = server_socket.accept()
        print(f"\nNew connection from {client_ip}:{client_port}")
        try_handle_client(client_socket)


def print_help():
    print(f"Usage: {sys.argv[0]} [OPTIONS] [PORT]")
    print()
    print("Options:")
    print("--public     allow external connections")
    print("--help       prints this info")


if __name__ == "__main__":
    ip = "localhost"
    port = DEFAULT_PORT

    for arg in sys.argv[1:]:
        if arg == "--help":
            print("Lunabotics server script")
            print()
            print_help()
            exit(1)
        elif arg == "--public":
            ip = "0.0.0.0"  # allows external connections
        elif arg.isdigit():
            if port == DEFAULT_PORT:
                port = int(arg)
            else:
                print(f"Cannot set port twice, remove or fix option {arg}")
                exit(1)
        else:
            print(f'Unknown option: "{arg}"')
            print()
            print_help()
            exit(1)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        start_server(server_socket, ip, port)
    except KeyboardInterrupt:
        server_socket.shutdown(socket.SHUT_RDWR)
        server_socket.close()
        print("\nFinished gracefully.")
