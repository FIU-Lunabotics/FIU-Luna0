#!/usr/bin/env python3
import socket
import sys
import time
import pickle

import evdev
import evdev.ecodes as ecodes

import consts
from rover_state import RoverState
from event import AxisEvent, ButtonEvent

DELAY_US = 5000  # time to delay sending state to server


def read_joystick(controller: evdev.InputDevice, c_socket: socket.socket):
    """Reads events from given device, then sends state to given socket"""
    axis_info = controller.capabilities(absinfo=True)[ecodes.EV_ABS]
    state = RoverState()  # track current rover state

    last_usec = 0  # track when last event was
    # update state with each input event received, and send latest state when enough time
    # has elapsed, to not overload server/arduino
    for input in controller.read_loop():
        # create correspoding event object depending on input type
        match input.type:
            case ecodes.EV_ABS:  # absolute (joysticks)
                event = AxisEvent(input.code, input.value, axis_info)
            case ecodes.EV_KEY:  # key (button)
                event = ButtonEvent(input.code, input.value)
            case _:  # not an event we care for
                continue

        state.take_event(event)

        # send current state over when enough time has passed
        if input.usec > last_usec + DELAY_US or input.usec < last_usec:
            c_socket.sendall(pickle.dumps(state))
            last_usec = input.usec
            print(state)


def find_controller() -> evdev.InputDevice:
    """
    Selects first device with axis and button capabilities as controller and
    returns that, otherwise raises FileNotFoundError
    """
    controller: evdev.InputDevice
    for path in evdev.list_devices():
        device = evdev.InputDevice(path)
        # check if device has axis movement (joysticks)
        capabilities = device.capabilities(absinfo=False)
        if ecodes.EV_ABS in capabilities and ecodes.EV_KEY in capabilities:
            controller = device
            break
    else:  # no controller found!
        raise FileNotFoundError

    return controller


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
            controller = find_controller()
            print(f"Controller found: {controller.name}")

            read_joystick(controller, c_socket)
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
    server_port = consts.DEFAULT_PORT

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
