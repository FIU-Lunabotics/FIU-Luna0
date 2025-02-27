# for now, unified client server docker file
FROM ros:jazzy AS builder

ENV DEBIAN_FRONTEND=noninteractive
# TODO: Read up on https://hub.docker.com/_/ros

# dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \

# mkdir and copy src to it
WORKDIR /app
COPY . /app
