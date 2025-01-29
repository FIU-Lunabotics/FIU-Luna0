# FIU_Lunabotics :D

Programming Tree for FIU Lunabotics Rover

## Setup

Make sure you have:

- Linux is required, the controller code uses Linux's native [evdev interface](https://en.wikipedia.org/wiki/Evdev).
- Either `pip` or manually installed the requirements from your distro.

### Pip

- Install `python3-pip` (or equiv.), if too old, do
  `pip3 install --upgrade pip` after.

Then run:

```bash
pip install --user -r requirements.txt
```

## Running

On server (PC which has controller connected to it.) run:

```bash
DEBUG_LEVEL=INFO ./controller/server.py --public
```

On client (Nano) run:

```bash
DEBUG_LEVEL=INFO  ./controller/client.py [SERVER_IP]
```

> [!NOTE]  
> When in development, you can set different logging levels in `.env` by
> prefixing the commands above with `DEBUG_LEVEL=INFO`

To see all available options, both scripts support `--help`.
