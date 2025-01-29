#!/usr/bin/env python3
import pickle
import socket
import sys
import time

from evdev import events
import util

logger = util.init_logger()


def react_to_event(event_type: int, code: int, value: int):
    if event_type == events.EV_KEY:
        action = "pressed" if value == 1 else "released"

        if util.button_north(code):
            logger.info(f"{action} north button")
        elif util.button_east(code):
            logger.info(f"{action} east button")
        elif util.button_south(code):
            logger.info(f"{action} south button")
        elif util.button_west(code):
            logger.info(f"{action} west button")
        elif util.button_lbumper(code):
            logger.info(f"{action} left bumper")
        elif util.button_rbumper(code):
            logger.info(f"{action} right bumper")
        elif util.button_ltrigger(code):
            logger.info(f"{action} left trigger")
        elif util.button_rtrigger(code):
            logger.info(f"{action} right trigger")
        elif util.button_select(code):
            logger.info(f"{action} select")
        elif util.button_start(code):
            logger.info(f"{action} start")
    elif event_type == events.EV_ABS:
        dpad_action = "released" if value == 0 else "pressed"

        if util.dpad_x(code):
            logger.info(f"{dpad_action} dpad x {value}")
        elif util.dpad_y(code):
            logger.info(f"{dpad_action} dpad y {value}")
        elif util.joy_left_x(code):
            logger.info(f"moved left joystick x {value}")
        elif util.joy_left_y(code):
            logger.info(f"moved left joystick y {value}")
        elif util.joy_right_x(code):
            logger.info(f"moved right joystick x {value}")
        elif util.joy_right_y(code):
            logger.info(f"moved right joystick y {value}")
    else:
        logger.info("idk bruh")


def connect_to_server(client_socket: socket.socket, ip: str, port: int):
    """
    Only returns when connection is lost. And therefore should be retried.
    """
    client_socket.connect((ip, port))
    logger.info("Connected successfully.")

    while True:
        data = client_socket.recv(1024)
        if len(data) == 0:  # did not receive any data, server prob closed
            break

        (event_type, code, value) = pickle.loads(data)
        react_to_event(event_type, code, value)


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
                logger.warning("Oops! Connection lost.")
                client_socket.shutdown(socket.SHUT_RDWR)
            except ConnectionRefusedError:
                logger.warning("Oops, connection was refused, is the server up?")
            except ConnectionResetError:
                logger.warning(
                    "Oops, connection reset, did server restart? Trying again."
                )
            except socket.gaierror:
                fatal_help(f'Invalid server IP: "{server_ip}"')
                break
            finally:
                client_socket.close()
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nFinished gracefully.")
