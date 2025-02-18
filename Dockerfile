# for now, unified client server docker file
FROM debian:bookworm AS builder

ENV DEBIAN_FRONTEND=noninteractive

# dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  cmake \
  ninja-build \
  libboost-dev \
  libboost-system-dev \
  libboost-thread-dev \
  pkg-config \
  libprotobuf-dev \
  protobuf-compiler \
  protobuf-compiler-grpc \
  libgrpc++-dev \
  libevdev-dev \
  meson \
  ninja-build

# mkdir and copy src to it
WORKDIR /app
COPY . /app

# build
# RUN rm -rf build && \
#   mkdir build && \
#   cd build && \
#   meson setup .. && \
#   ninja
