# ![logo](https://media.githubusercontent.com/media/ModischFabrications/CutSolverFrontend/main/src/assets/logo.svg) CutSolver

[![CI/CD](https://github.com/ModischFabrications/CutSolver/actions/workflows/ci.yml/badge.svg)](https://github.com/ModischFabrications/CutSolver/actions/workflows/ci.yml)
[![Docker Image Version](https://img.shields.io/docker/v/modischfabrications/cutsolver?sort=semver)](https://hub.docker.com/r/modischfabrications/cutsolver)
[![Pulls from DockerHub](https://img.shields.io/docker/pulls/modischfabrications/cutsolver)](https://hub.docker.com/r/modischfabrications/cutsolver)

*This is a backend, see [CutSolverFrontend](https://github.com/ModischFabrications/CutSolverFrontend) for a human usable
version.*

This API can be used to solve the common problem of finding the perfect placement of cuts for specified lengths.
It seems like no other free service tackles this specific problem in an easy-to-use format, so this is my attempt.

*You are very welcome to share how you use this tool!*

![cutsolver](https://github.com/ModischFabrications/CutSolver/raw/main/docs/cutsolver.svg)

This Solver is using integers exclusively, as there is no need for arbitrary precision (yet).
Feel free to shift your numbers a few decimals if you need fractions.
It has no concept of units, so you can use whatever you want.

*Nerd talk*: This is the 2D "Cutting Stock Problem", which is NP-hard. It can be reduced to the Bin-Packing-Problem (
BPP).
No algorithm exists to calculate a perfect solution in polynomial time, therefore brute force (perfect
solution) is used for small jobs (usually <12 entries) and FFD (fast solution) für larger ones.
Don't be surprised if you get different results, many combinations have equal trimmings and are therefore seen as
equally good.

## Usage/Hosting

Feel free to run manually, but the easiest (and advised) way to deploy this is by using Docker and pulling an up-to-date
image.

Send POST-Requests to `[localhost]/solve` to get your results, see `/docs` for further information.

Also see [example job and result](/tests/res) from tests.

### Docker

You don't need to check out this repository and build your own image, I am pushing prebuild ones to Docker Hub.
Download and start this container by using the provided docker-compose file or
with `docker run [--rm -it] -p80:80 modischfabrications/cutsolver:latest`.

Note: Replace `latest` with a version number if you depend on this interface, I can guarantee you that the interface
will change randomly. It's more or less stable since the 1.0 release, but be ready for the unexpected.

Both `linux/amd64` and `linux/arm/v7` are currently supported, more will be build whenever I get around to it, message
me if you need another architecture.

## Performance

If it can run Docker it will probably be able to run CutSolver.
1 vCPU with 500MB RAM should be fine for small workloads.

Runtimes strongly depend on the single-core performance of your CPU.
You can expect 12 entries to be solved after ~1s with `bruteforce`and <0.1s with `FFD` for generic desktops, slower on
weaker machines.
Multiple cores won't speed up job time, but will enable efficient solving of parallel jobs.

The thresholds that decide which jobs are solved which way are defined in constants.py and can be passed as env,
see [docker-compose.yml](/docker-compose.yml) for details.

## Contributing

Feel free to contact me or make a pull-request if you want to participate.

Sponsoring and/or paid development is also very welcome, feel free to reach out.

### Git

Install pre-commit with `pre-commit install && pre-commit install -t pre-push`.
You might need to replace `#!/bin/sh` with `#!/usr/bin/env sh` in the resulting *.legacy file on Windows.

All obvious errors should be checked and or fixed by pre-commit, execute `pre-commit run --all-files --hook-stage push`
to run manually.

Change version number in main.py:version for newer releases, git tags will be created automatically.

### Testing

Remember to test your changes using `pytest`. This will happen automatically both in pre-commit and in CI/CD, but manual
tests will reduce iteration times.

Code coverage and runtimes can be checked
using `pipenv run python -m pytest --durations=5 --cov=app/ --cov-report term-missing`.
Make sure that all critical parts of the code are covered, at v1.0.1 it is at 94%.

### Development Docker Images

1. Build and start this image using `docker-compose up`
2. wait a while for dependencies to build... (1000s)
3. Hope that everything works

` docker run --rm -it -p 8000:80 $(docker build -q .)` is also useful to start a temporary container for testing.

### Push Production Docker Images

Docker Hub Images should be updated automatically, but feel free to build yourself should everything else fail.
Adding "[skip ci]" to the commit message will prevent any ci builds should the need arise.
Thankfully, local builds are easy with the modern `buildx` workflow.

Installation of a multibuilder (once):

```
docker buildx create --name multibuilder --use
docker buildx inspect multibuilder --bootstrap
```

Build and push the new multi-arch image with the following steps (add version, e.g. v0.3.7):

```
docker login -u modischfabrications
docker buildx build --platform linux/amd64,linux/arm/v7,linux/arm64 \
    -t modischfabrications/cutsolver:<VERSION> \
    -t modischfabrications/cutsolver:latest --push .
```

Wait a while for every dependency to build (~1000s) and all layers to be pushed (~400s). Feel free to drink some water
and be bored, that's healthy from time to time.

Check [Docker Hub](https://hub.docker.com/r/modischfabrications/cutsolver) to see results.

## Dependencies

*Everything should be handled by Docker and/or pipenv.*

This project uses:

* [FastAPI](https://github.com/tiangolo/fastapi): easy API (this includes much more!)
* [Uvicorn](https://github.com/encode/uvicorn): async web server

Also used for development is:

* [pipenv](https://github.com/pypa/pipenv): library management
* [httpie](https://github.com/jakubroztocil/httpie): simpler `curl` for docker healthchecks
* [pytest](https://pytest.org): A lot nicer unit tests
* [flake8](https://flake8.pycqa.org/): Linting
* [requests](https://requests.readthedocs.io/): simple HTTP requests
* [black](https://github.com/psf/black): uncompromising code formatter; currently unused

## External links

<https://scipbook.readthedocs.io/en/latest/bpp.html>
