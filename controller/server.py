#!/usr/bin/env python3
import socket
import threading
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

    CODE_LEFT_TRIGGER = 312
    CODE_LEFT_BUMPER = 310
    CODE_RIGHT_TRIGGER = 313
    CODE_RIGHT_BUMPER = 311

    CODE_LEFT_JOY_HORI = 0
    CODE_LEFT_JOY_VERT = 1
    CODE_RIGHT_JOY_HORI = 3
    CODE_RIGHT_JOY_VERT = 4


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
    event = joystick.read(event_size)
    while event:
        client_socket.send(event)

        # FIXME: will panic if controller is disconnected
        event = joystick.read(event_size)  # get next event


def try_handle_client(client_socket: socket.socket, first_fail: bool = True):
    try:
        read_joystick(client_socket)
    except FileNotFoundError:
        if first_fail:
            print("Controller not found, connect pls.")
        time.sleep(2)
        try_handle_client(client_socket, False)
        # Optionally, receive data from client
        # data = client_socket.recv(1024)
        # print("Received from client:", data.decode())


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOSTNAME, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOSTNAME}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        thread = threading.Thread(target=try_handle_client, args=(client_socket,))
        thread.start()


if __name__ == "__main__":
    print("Press Ctrl+C to stop.\n\n")
    try:
        start_server()
    except KeyboardInterrupt:
        print("\nFinished gracefully.")
        os._exit(0)
