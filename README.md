# Luna0

Lunabotics rover code using [ROS2] Jazzy in C++

## Building

> [!WARNING]
> You will need to [install ROS2] Jazzy (or use the ROS docker image
> and build a dev container).

At this repository root, run:

```bash
colcon build
```

Which will compile the packages and nodes we have, and give you a source-able
script in `./install` (change file name for your shell if needed):

```bash
source install/local_setup.bash
```

Then, to run you use the syntax:

```bash
ros2 run luna_controller controller_client
```

Where that is `ros2 run <package> <node>`. You can see all available packages
and nodes like so:

```bash
ros2 pkg executables | grep luna
```

## Development

> [!NOTE]
> For development, container usage is preferred, unclear if ports or Bluetooth
> will be an issue at this time. End result will be a local build on both
> client and server at competition.

### Docker Images

If you would like to just run through Docker

```bash
docker build -t luna .
docker run -it luna /bin/bash
```

Once the image is built and running follow the [building] steps.

### Run Dev Container

On Linux, run `./run_dev_container.sh`. On Windows, right-click and run
`run_dev_container.bat`. For this script you will need:

- Visual Studio Code
- [Dev Container Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

[ROS2]: https://wiki.ros.org/ROS/Introduction
[install ROS2]: https://docs.ros.org/en/jazzy/Installation.html
[building]: #building
