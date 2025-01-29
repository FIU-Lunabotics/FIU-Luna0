#!/usr/bin/env python3
import pickle
import socket
import sys
import time

import evdev
from evdev import events

import util
from util import DEFAULT_PORT

logger = util.init_logger()


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

    logger.info(f"Controller found: {controller.name}")
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
                logger.warning("Controller not found, connect pls.")
        except BrokenPipeError:
            logger.error("Failed to send controller event, did client disconnect?")
            break
        except OSError as err:
            if err.errno == 19:
                logger.warning("Oops! controller no longer exists, did it disconnect?")
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
        logger.info(f"New connection from {client_ip}:{client_port}")
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
    port = DEFAULT_PORT

    for arg in sys.argv[1:]:
        if arg == "--help":
            fatal_help("Lunabotics server script")
        elif arg == "--public":
            ip = "0.0.0.0"  # allows external connections
        elif arg.isdigit():
            if port == DEFAULT_PORT:
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
        print("Finished gracefully.")
