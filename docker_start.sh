#!/usr/bin/env bash

docker run --name cutsolver -d -p 5000:5000 --rm cutsolver:latest
# docker run --name cutsolver -it -p 5000:5000 --rm cutsolver:latest
