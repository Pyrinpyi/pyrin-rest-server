@echo off
SET PYIPAD_HOST_1=host.docker.internal
docker run --rm -p 8000:8000 pyrin-rest-server:latest
