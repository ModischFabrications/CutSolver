#!/bin/sh
# bash not available in alpine

# flask only (debug)
flask run --host=0.0.0.0

# gunicorn deployment
# TODO exec gunicorn ...
