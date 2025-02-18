# Luna0

## Setup

### Local

```bash
meson setup build
ninja -C build
```

> [!NOTE]
> For protobuf compilation remove all files in `proto` with the exception of `luna.proto` and run:
> `protoc -I . --cpp_out=. --grpc_out=. --plugin=protoc-gen-grpc="{{/path/to/grpc_cpp_plugin}}" proto/luna.proto`

### Container

> [!NOTE]
> For development, container usage is preferred, unclear if ports or Bluetooth will be an issue at this time.
> End result will be a local build on both client and server at competition.

#### Docker Images

If you would like to just run through Docker

```bash
docker build -t luna .
docker run -it luna /bin/bash
```

Once the image is built and running:

```bash
meson setup build
ninja -C build
```

#### Run Dev Container

On Linux, run `./run_dev_container.sh`. On Windows, right-click and run `run_dev_container.bat`. For this script you will need:

- Visual Studio Code
- [Dev Container Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

## Running

<!-- TODO: idek bruh u got this tho -->
