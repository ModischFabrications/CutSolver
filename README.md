# CutSolver

[![Travis (.org)](https://img.shields.io/travis/ModischFabrications/cutsolver.svg)](https://travis-ci.org/ModischFabrications/CutSolver)
[![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/modischfabrications/cutsolver.svg)](https://cloud.docker.com/repository/docker/modischfabrications/cutsolver)
[![Docker Image Size](https://images.microbadger.com/badges/image/modischfabrications/cutsolver.svg)](https://cloud.docker.com/repository/docker/modischfabrications/cutsolver)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/11d689cd44b0407fac23d537ca0f239f)](https://app.codacy.com/app/ModischFabrications/CutSolver)
[![Rating](https://img.shields.io/badge/rating-awesome-brightgreen.svg)](#)

This API can be used to solve the 2D "Cutting Stock Problem", which is NP-hard. It can be reduced to the Bin-Packing-Problem (BPP).
It seems like no other free service tackles this specific problem in an easy to use format, so this is my attempt. 

No efficient algorithm exists to calculate a perfect solution in an acceptable timeframe, therefore brute force (perfect solution) 
is used for small jobs and a heuristic (fast solution) für larger ones. Don't be surprised if you get different results, 
many combinations have equal trimmings and are therefore seen as equally good. 

This Solver is using ints exclusively, as there is no need for arbitrary precision yet. 
It also has no concept of units so you can use whatever you want.
Try using mm instead of cm if you have fractions.

![cutsolver](https://user-images.githubusercontent.com/25404728/53304884-fb9c4980-387a-11e9-9a49-330369befc44.png)

## Usage
*This is a backend, see [CutSolverFrontend](https://github.com/ModischFabrications/CutSolverFrontend) for a human usable version.*

Send POST-Requests to `[localhost]/solve`, see `/docs` for further informations.

The easiest (and advised) way to deploy this is by using Docker.

### Docker Hub
**Now with 100% more Multiarchitecture!**  
Both `linux/amd64` and `linux/arm/v7` are currently supported, message me if you use another platform. 

You don't need to checkout this repository, I am building images and pushing them to Docker Hub.
Download and start this container by using the provided docker-compose file or running: 
`docker run [--rm -it] -p80:80 modischfabrications/cutsolver:latest`. 

Note: Replace `latest` with a version number if you depend on this interface, I can guarantee you that the interface 
will change randomly however I think is best at that moment.

### Local build
1. Build and start this image using `docker-compose up`
2. wait a while for uvloop to build... (1000s)
3. See usage for interactions.

## Developing
Feel free to contact me or make a pull-request if you want to participate in it.

Make sure to execute `pipenv lock -r > requirements.txt && pipenv lock -r --dev > dev-requirements.txt` when updating "Pipfile".

Rebuild the docker image with `docker-compose up --build` and check uncompressed image size with `docker-compose images`.

Update Docker Hub with the following steps:
1. Installation (once)
    1. check "experimental features" in Docker Desktop
    2. `docker buildx create --name multibuilder --use`
2. `docker login -u modischfabrications`
3. `docker buildx build --platform linux/amd64,linux/arm/v7 -t modischfabrications/cutsolver:latest --push .`
4. wait a while for uvloop to build... (1000s)
5. wait for all layers to be pushed... (400s)
6. Check <https://hub.docker.com/repository/docker/modischfabrications/cutsolver>

## Dependencies
*Everything should be handled by Docker*

This project uses:
*   [pipenv](https://github.com/pypa/pipenv): library management
*   [FastAPI](https://github.com/tiangolo/fastapi): easy webservice (this includes much more!)

## External links
<https://scipbook.readthedocs.io/en/latest/bpp.html>
