#!/usr/bin/env bash

# uses httpie (which is a lot nicer than curl!)
http POST :8000/solve < testjob_L.json
