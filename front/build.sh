#!/usr/bin/env bash
exec docker run -it --user "$(id -u)" -v "$PWD:/dev_mount" node:16.5.0 /bin/bash -c "cd /dev_mount; npm install && npm run build"
