#!/usr/bin/env python
import pickle
import socket
import sys

from event import AxisEvent, ButtonEvent
from rover_state import RoverState
import util

state = RoverState()


def react_to_event(event: AxisEvent | ButtonEvent):
    # print(event._code) # debug
    state.take_event(event)
    print(state)
    # TODO: send data to arduino using state.get_arduino_data()


def try_handle_client(client_socket: socket.socket):
    while True:
        data = client_socket.recv(1024)
        if len(data) == 0:  # did not receive any data, server prob closed
            break

        event = pickle.loads(data)
        react_to_event(event)


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


def fatal_help(message: str):
    """
    Prints help with the given message at the top,
    then exits with error status (1)
    """
    print(message)
    print()
    print(f"Usage: {sys.argv[0]} [OPTIONS] [PORT]")
    print()
    print("Options:")
    print("--public     allow external connections")
    print("--help       prints this info")
    exit(1)


if __name__ == "__main__":
    ip = "localhost"
    port = util.DEFAULT_PORT

    for arg in sys.argv[1:]:
        if arg == "--help":
            fatal_help("Lunabotics server script")
        elif arg == "--public":
            ip = "0.0.0.0"  # allows external connections
        elif arg.isdigit():
            if port == util.DEFAULT_PORT:
                port = int(arg)
            else:
                fatal_help("Cannot set port twice, remove or fix numbers")
        else:
            fatal_help(f'Unknown option: "{arg}"')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        start_server(server_socket, ip, port)
    except KeyboardInterrupt:
        server_socket.shutdown(socket.SHUT_RDWR)
        server_socket.close()
        print("\nFinished gracefully.")
