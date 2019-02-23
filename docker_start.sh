#!/usr/bin/env bash

docker run --name cutsolver -d -p 80:80 --rm cutsolver:latest

# -it: interactive (debugging)
# -d: background (normal use)
# --restart=always: use when deploying
