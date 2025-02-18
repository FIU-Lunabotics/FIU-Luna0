#!/usr/bin/env bash

echo "building image"
docker build -t luna .

echo "running container"
docker run -it luna /bin/bash

echo "container running"
