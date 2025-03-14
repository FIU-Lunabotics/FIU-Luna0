# Architecture

We will have the server (our Raspberry Pi) collecting info from a controller
client (some laptop) then handles it and sends it to the Arduinos controlling
our motors and more.

## `server.py`

To configure and see usage run:

```bash
server.py --help
```

### Collect

- From client
  - Receive Axis and Button events
- From camera (TODO)
  - Get stream

### Disperse

- To client (TODO)
  - Camera data
- To Arduinos (TODO)
  - Events converted into PWM?

## `client.py`

To configure server IP/port and see usage run:

```bash
client.py --help
```

### Read / Process

- Controller events from evdev
- Controller config (deadzone, button layout) (maybe)

### Send

- To server
  - Send standardized Axis and Button events
    [serialized](https://en.wikipedia.org/wiki/Serialization) through pickle
