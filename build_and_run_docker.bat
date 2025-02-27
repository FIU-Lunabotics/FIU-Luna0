@echo off
echo Building Docker image
docker build -t luna .

echo Running Docker container
docker run -it luna /bin/bash

echo Container is running
pause
