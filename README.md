# CutSolver

[![Docker Image Version](https://img.shields.io/docker/v/modischfabrications/cutsolver.svg)](https://hub.docker.com/repository/docker/modischfabrications/cutsolver)
[![Docker Image Size](https://img.shields.io/docker/image-size/modischfabrications/cutsolver.svg)](https://hub.docker.com/repository/docker/modischfabrications/cutsolver)
![Rating](https://img.shields.io/badge/rating-awesome-brightgreen.svg)

This API can be used to solve the common problem of finding the perfect placement of cuts for specified lengths.
It seems like no other free service tackles this specific problem in an easy-to-use format, so this is my attempt.

You are very welcome to share how you use this tool!

![cutsolver](https://user-images.githubusercontent.com/25404728/53304884-fb9c4980-387a-11e9-9a49-330369befc44.png)

This Solver is using integers exclusively, as there is no need for arbitrary precision (yet).
Feel free to shift your numbers a few decimals if you need fractions.
It has no concept of units, so you can use whatever you want.

*Nerd talk*: This is the 2D "Cutting Stock Problem", which is NP-hard. It can be reduced to the Bin-Packing-Problem (
BPP).
No efficient algorithm exists to calculate a perfect solution in an acceptable timeframe, therefore brute force (perfect
solution)
is used for small jobs and a heuristic (fast solution) für larger ones. Don't be surprised if you get different results,
many combinations have equal trimmings and are therefore seen as equally good.

## Usage

*This is a backend, see [CutSolverFrontend](https://github.com/ModischFabrications/CutSolverFrontend) for a human usable
version.*

The easiest (and advised) way to deploy this is by using Docker and pulling an up-to-date image.

Send POST-Requests to `[localhost]/solve` to get your results, see `/docs` for further information.

Solver `bruteforce` guarantees the ideal solution, but is very expensive and works only for <13 entries. `FFD` is a lot
faster and works for larger sets, but won't
guarantee perfect results.

### Docker Hub

You don't need to check out this repository, I am building images and pushing them to Docker Hub.

**Now with 100% more Multiarchitecture!**

Both `linux/amd64` and `linux/arm/v7` are currently supported, some will be build whenever comfortable, message me if
you need another platform.

Download and start this container by using the provided docker-compose file or running:
`docker run [--rm -it] -p80:80 modischfabrications/cutsolver:latest`.

Note: Replace `latest` with a version number if you depend on this interface, I can guarantee you that the interface
will change randomly. It's not like I know what I'm doing, it's more like a learning curve.

### Local build
1. Build and start this image using `docker-compose up`
2. wait a while for uvloop to build... (1000s)
3. See usage for interactions.

## Contributing
Feel free to contact me or make a pull-request if you want to participate.

Install pre-commit with `pre-commit install && pre-commit install -t pre-push`.

Change version number in:
1. main.py:version
2. git tag
3. Dockerfile?

This should be checked and or fixed by pre-commit, execute `pre-commit run --all-files --hook-stage push` to run manually.

### Prebuild docker images

Docker Hub Images should be updated automatically, but that doesn't work at the moment (see #44).
That isn't as bad as it sounds, because local builds are easily manageable with `buildx`.

Installation of a multibuilder (once):

```
docker buildx create --name multibuilder --use
docker buildx inspect multibuilder --bootstrap
```

Build and push the new multi-arch image with the following steps (add version, e.g. v0.3.7):

```
docker login -u modischfabrications
docker buildx build --platform linux/amd64,linux/arm/v7 \
    -t modischfabrications/cutsolver:<VERSION> \
    -t modischfabrications/cutsolver:latest --push .
```

Wait a while for every dependency to build (~1000s) and all layers to be pushed (~400s).

Want to check the size prior to pushing it?
Rebuild the docker image with `docker-compose up --build` and check uncompressed image size with `docker-compose images`
.

Check [Docker Hub](https://hub.docker.com/repository/docker/modischfabrications/cutsolver) to see results.

## Dependencies

*Everything should be handled by Docker*

This project uses:

* [pipenv](https://github.com/pypa/pipenv): library management
* [FastAPI](https://github.com/tiangolo/fastapi): easy webservice (this includes much more!)
* [httpie](https://github.com/jakubroztocil/httpie): curl-like for docker healthcheck

## External links
<https://scipbook.readthedocs.io/en/latest/bpp.html>
