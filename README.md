# FIU_Lunabotics :D

Programming Tree for FIU Lunabotics Rover

## Setup

Make sure you have:

- Linux, as the controller code uses Linux's native [evdev interface](https://en.wikipedia.org/wiki/Evdev).
- Either `pip` or manually installed the requirements from your distro.

### Pip

- Install `python3-pip` (or equivalent)

Then run:

```bash
pip install --user -r requirements.txt
```

## Running

On client (PC which has controller connected to it.) run:

```bash
./controller/client.py [SERVER_IP]
```

On server (rover/Raspberry Pi) run:

```bash
./controller/server.py --public
```

To see all available options, both scripts support `--help`.
