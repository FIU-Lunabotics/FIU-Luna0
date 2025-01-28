#!/usr/bin/env python3
import pickle
import socket
import time

import evdev
from evdev import events

HOSTNAME = "localhost"
PORT = 5000


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
        data = (event.type, event.code, event.value)
        if (  # all-zero events and event types 2 and 4 are ignored.
            sum(data) != 0 and event.type % 2 != 0
        ):
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


def start_server(server_socket: socket.socket):
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOSTNAME, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOSTNAME}:{PORT}")
    print("Press Ctrl+C to stop.")

    while True:
        client_socket, (client_ip, client_port) = server_socket.accept()
        print(f"\nNew connection from {client_ip}:{client_port}")
        try_handle_client(client_socket)


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        start_server(server_socket)
    except KeyboardInterrupt:
        server_socket.shutdown(socket.SHUT_RDWR)
        server_socket.close()
        print("\nFinished gracefully.")
