# Architecture

The focus is on having the server carry the grunt of work if possible
(gathering controller events, converting them to normalized ones, etc.) and
having the client (our dinky Nano) be more of a relay.

## `server.py`

To configure and see usage run:

```bash
server.py --help
```

### Read / Process

- Controller events from evdev
- Controller config (deadzone, button layout)

### Send

- Connect to client
- Send standardized Axis and Button events
  [serialized](https://en.wikipedia.org/wiki/Serialization) through pickle

## `client.py`

To configure server IP/port and see usage run:

```bash
client.py --help
```

### Collect

- From server
  - Receive Axis and Button events
- From camera (TODO)
  - Get stream

### Disperse

- To server (TODO)
  - Camera data
- To Arduinos (TODO)
  - Events converted into PWM?
