#!/usr/bin/env python
import pickle
import serial
import serial.serialutil as serialutil
import socket
import sys

import consts

RECV_SIZE = 1024


def try_handle_client(client_socket: socket.socket):
    try:
        arduino = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=0.1)
    except serialutil.SerialException:
        arduino = None
        print("No arduino found! Only debugging")

    while True:
        # get all data possible
        chunks = []
        while True:
            chunk = client_socket.recv(RECV_SIZE)
            if not chunk:  # no data to receive
                break

            chunks.append(chunk)
            if len(chunk) < RECV_SIZE:
                break

        # convert all chunks into one byte array to unpickle
        data = b"".join(chunks)
        if not data:  # did not receive any data, server prob closed
            break

        state = pickle.loads(data)

        # send final resulting state to Arduino
        if arduino:
            arduino.write(state.get_arduino_data())
            print(f"Arduino: {arduino.read_all()}")


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
    port = consts.DEFAULT_PORT

    for arg in sys.argv[1:]:
        if arg == "--help":
            fatal_help("Lunabotics server script")
        elif arg == "--public":
            ip = "0.0.0.0"  # allows external connections
        elif arg.isdigit():
            if port == consts.DEFAULT_PORT:
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
