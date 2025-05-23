# Architecture

We will have the server (our Raspberry Pi) collecting info from a controller
client (some linux computer) then handles it and sends it to the Arduinos controlling
our motors and more.

## Server (`server.py`)

To configure and see usage run:

```bash
server.py --help
```

### Collect

- From client
  - Current rover control state

### Disperse

- To Arduinos
  - The current state formatted as below

| Byte index | Value                 |
| ---------- | --------------------- |
| 0          | Start Byte            |
| 2          | Joystick Left X       |
| 3          | Joystick Left Y       |
| 5          | Joystick Right Y      |
| 6          | Trigger               |
| 7          | End Byte              |

#### Bitmask

We use the Start and End Bytes as data validation in the form of a buffer as well as using specific bits to transmit button states.

| Byte      | Buffer Value     |
| --------- | ---------------- |
| Start     | 0b10101000       |
| End       | 0b00010101       |

| Bit index | Value     |
| --------- | --------- |
| 0         | Tank mode |

## Client (`client.py`)

To configure server IP/port and see usage run:

```bash
client.py --help
```

### Read / Process

- Controller events from evdev
- Update current state on each input event
- TODO: Controller config (deadzone, button layout) (maybe)

### Send

- To server
  - Send the latest state
    [serialized](https://en.wikipedia.org/wiki/Serialization) through pickle

# Architecture

We will have the server (our Raspberry Pi) collecting info from a controller
client (some laptop) then handles it and sends it to the Arduinos controlling
our motors and more.

## Server (`server.py`)

To configure and see usage run:

```bash
server.py --help
```

### Collect

- From client
  - Current rover control state

### Disperse

- To Arduinos
  - The current state formatted as below

| Byte index | Value                 |
| ---------- | --------------------- |
| 0          | 255                   |
| 1          | [Bitmask1](#bitmask1) |
| 2          | Joystick Left X       |
| 3          | Joystick Left Y       |
| 4          | Joystick Right X      |
| 5          | Joystick Right Y      |
| 6          | 0 (_Placeholder_)     |
| 7          | 255                   |

#### Bitmask1

| Bit index | Value     |
| --------- | --------- |
| 0         | Tank mode |

## Client (`client.py`)

To configure server IP/port and see usage run:

```bash
client.py --help
```

### Read / Process

- Controller events from evdev
- Update current state on each input event
- TODO: Controller config (deadzone, button layout) (maybe)

### Send

- To server
  - Send the latest state
    [serialized](https://en.wikipedia.org/wiki/Serialization) through pickle
