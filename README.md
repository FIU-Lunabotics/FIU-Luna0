# FIU_Lunabotics :D

Programming Tree for FIU Lunabotics Rover

## Controller

### Prereqs

- Linux is required, the controller code uses Linux's native [evdev interface](https://en.wikipedia.org/wiki/Evdev).
- Pip (On Ubuntu: `python3-pip`, although if too old do `pip3 install --upgrade pip`)

### Setup

After you have the [prerequisites](#prereqs), run:

```bash
pip install --user -r requirements.txt
```

### Running

On server (PC which has controller connected to it.) run:

```bash
./controller/server.py
```

On client (Nano) run:

```bash
./controller/client.py
```
