# FIU_Lunabotics :D

Programming Tree for FIU Lunabotics Rover

## Setup

Make sure you have:

On Controller
- Linux, as the controller code uses Linux [evdev].
- Python (should have it on most Linux distros)

On Server
- Linux, just the same
- Python, just the same
- Visual Studio Code with PlatformIO installed (make sure to open folder through PIO Home as project) onto the SERVER
- VS Code, Coderunner extension

Connect the Arduino Mega 2560 to the Raspberry Pi 5 via USB as we use Serial input and the USB is the power source. 

### Python Virtual Environment

To install dependencies separate from your system, create a virtual environment
in the folder `.venv` (Do this on both the Server and Client ends):

Install:

```bash
sudo apt install python3-venv
```

To create:

```bash
python -m venv .venv
```
To check if your venv creation was successful, within the directory use:

```bash
ls -A
```

Then activate it like so (must be done every terminal session):

```bash
source .venv/bin/activate
```

And finally, install the dependencies:

```bash
pip install -r requirements.txt
```

To exit:

```bash
deactivate
```

> [!TIP]
> The Python evdev bindings install may fail (at least on Fedora) if you are
> missing Python.h, to fix this, install `python-devel`

## Running

### Arduino

FIRST, Click "Build" and then "Upload" at the bottom of your environment. The arduino code should now be running. 

### Linux

THEN, On client (PC which has controller connected to it) run:

```bash
./controller/client.py [SERVER_IP]
```

On server (rover/Raspberry Pi with Arduino connected to it) run:

```bash
./controller/server.py --public
```

To see all available options, both scripts support `--help`.

## Developing
You can use the Arduino IDE instead of PlatformIO on VSCode, or [arduino-cli] if you're feeling adventurous.

Make sure you have read all READMEs, like this one and the one for the
controller [architecture](/controller/README.md).

Run `controller/client.py` and `controller/server.py` on their respective
machines (or the same one for quicker development.) Then _after_ `server.py`
has connected to the Arduino you can open PlatformIO or Arduino IDE and see its output.

_Sadly, the python script and the IDE fight over the Arduino so you may
need to stop one or the other and reopen during development._

[evdev]: https://en.wikipedia.org/wiki/Evdev
[arduino-cli]: https://github.com/arduino/arduino-cli
[PlatformIO]: https://docs.platformio.org/en/latest/