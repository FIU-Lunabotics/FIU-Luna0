#!/usr/bin/env python3
import socket
import sys
import time
import pickle

import evdev
from evdev import events

import util
from util import COALESCE_MS
from event import AxisEvent, ButtonEvent


def read_joystick(c_socket: socket.socket):
    controller: evdev.InputDevice
    # select first device with joysticks as controller
    for path in evdev.list_devices():
        device = evdev.InputDevice(path)
        # check if device has axis movement (joysticks)
        capabilities = device.capabilities(absinfo=False)
        if events.EV_ABS in capabilities and events.EV_KEY in capabilities:
            controller = device
            break
    else:
        raise FileNotFoundError

    print(f"Controller found: {controller.name}")

    axis_info = controller.capabilities(absinfo=True)[events.EV_ABS]
    last_abs_usec = 0  # use to ignore absolute events that happen too quick
    for event in controller.read_loop():
        if event.type == events.EV_ABS and (
            event.usec > last_abs_usec + COALESCE_MS or event.usec < last_abs_usec
        ):
            event = AxisEvent(event.code, event.value, axis_info)  # type:ignore
        elif event.type == events.EV_KEY:
            event = ButtonEvent(event.code, event.value)
        else:
            continue

        c_socket.sendall(pickle.dumps(event))


def connect_to_server(c_socket: socket.socket, ip: str, port: int):
    """
    Only returns when connection is lost. And therefore should be retried.
    """
    c_socket.connect((ip, port))
    print("\nConnected successfully.")

    # read (and send) controller input endlessly
    first_fail = True
    while True:  # preferred over recursively calling to avoid stack overflow
        try:
            read_joystick(c_socket)
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
