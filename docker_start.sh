#!/usr/bin/env bash

docker run --name cutsolver --restart=always -d -p 80:80 --rm cutsolver:latest
# docker run --name cutsolver -it -p 80:80 --rm cutsolver:latest

# -it: interactive (debugging)
# -d: background (normal use)
# --restart=always: use when deploying
