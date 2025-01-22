#!/usr/bin/env python3
from io import BufferedReader
import socket
import struct
import os
import time

HOSTNAME = "localhost"
PORT = 5000

# Joystick event struct byte representation
EVENT_FORMAT = "llHHi"


# change according to current controller
class EventCodes:
    EVENT_TYPE_BUTTON = 1
    EVENT_TYPE_JOYSTICK = 3  # or dpad for some reason

    VALUE_BUTTON_UP = 0
    VALUE_BUTTON_DOWN = 1

    CODE_LEFT_JOY_HORI = 0
    CODE_LEFT_JOY_VERT = 1
    CODE_RIGHT_JOY_HORI = 3
    CODE_RIGHT_JOY_VERT = 4

    CODE_DPAD_HORI = 16
    CODE_DPAD_VERT = 17

    CODE_LEFT_TRIGGER = 312
    CODE_LEFT_BUMPER = 310
    CODE_RIGHT_TRIGGER = 313
    CODE_RIGHT_BUMPER = 311


class ControllerLostError(BaseException):
    pass


def read_event(device: BufferedReader, event_size: int):
    try:
        return device.read(event_size)  # get next event
    except OSError as err:
        if err.errno == 19:
            raise ControllerLostError
        else:
            raise err


def read_joystick(client_socket: socket.socket):
    # read raw joystick events from first controller found
    PATH = "/dev/input/by-id/"

    controller = ""
    for dev in os.listdir(PATH):
        if dev.endswith("joystick"):
            controller = f"{PATH}{dev}"

    if not controller:
        raise FileNotFoundError

    # joystick reading logic from https://stackoverflow.com/questions/5060710/format-of-dev-input-event
    joystick = open(
        controller,
        "rb",
    )

    print("Controller found.")
    event_size = struct.calcsize(EVENT_FORMAT)
    event = read_event(joystick, event_size)
    while event:
        client_socket.sendall(event)
        event = read_event(joystick, event_size)


def try_handle_client(client_socket: socket.socket):
    first_fail = True
    while True:  # preferred over recursively calling to avoid stack overflow
        try:
            read_joystick(client_socket)
        except FileNotFoundError:
            if first_fail:
                print("Controller not found, connect pls.")
        except ControllerLostError:
            print("Oops! controller no longer exists, did it disconnect?")
        except BrokenPipeError:
            print("Failed to send controller event, did client disconnect?")
            break
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
