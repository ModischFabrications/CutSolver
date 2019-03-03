#!/usr/bin/env bash

docker run --name cutsolver --restart=always -d -p 5000:5000 --rm cutsolver:latest
# docker run --name cutsolver -it -p 5000:5000 --rm cutsolver:latest

# -it: interactive (debugging)
# -d: background (normal use)
# --restart=always: use when deploying
