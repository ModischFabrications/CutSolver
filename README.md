# CutSolver

[![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/modischfabrications/cutsolver.svg)](https://cloud.docker.com/repository/docker/modischfabrications/cutsolver)
[![Docker Image Size](https://images.microbadger.com/badges/image/modischfabrications/cutsolver.svg)](https://cloud.docker.com/repository/docker/modischfabrications/cutsolver)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/11d689cd44b0407fac23d537ca0f239f)](https://app.codacy.com/app/ModischFabrications/CutSolver)
[![Rating](https://img.shields.io/badge/rating-awesome-brightgreen.svg)](#)

This API can be used to solve the 2D "Cutting Stock Problem", which is NP-hard. It can be reduced to the Bin-Packing-Problem (BPP).

No efficient algorithm exists to calculate a perfect solution in an acceptable timeframe, therefore brute force (perfect solution) is used for small jobs and a heuristic (fast solution) für larger ones. 

This Solver is using ints exclusively, as there is no need for arbitrary precision yet. 
It also has no concept of units so you can use whatever you want.

## Usage
Make sure that you have installed Docker + Docker Compose.  

1. Build and start this image using `docker-compose up`
2. Send POST-Requests to `[localhost]/solve`, see `/docs` for further informations.

## Visualisation

![cutsolver](https://user-images.githubusercontent.com/25404728/53304884-fb9c4980-387a-11e9-9a49-330369befc44.png)
## Roadmap
### Support welcome
It seems like no other free service tackles this specific problem in an easy to use format, so this is my attempt. Feel free to contact me or make a pull-request if you want to participate in it.

### Declined
Having workers and a queue with pending jobs was considered but seemed useless, 
as ideally all requests have their own thread and a (by comparison) short calculation time.
This makes a queue useless. The same argumentation also holds true for a result-buffer.

## Contributing
Make sure to execute `pipenv lock --requirements > requirements.txt` when updating "Pipfile".

Rebuild the docker image with `docker-compose up --build` and check uncompressed image size with `docker-compose images`.

## Dependencies
*Everything should be handled by Docker*

This project uses:
* [pipenv](https://github.com/pypa/pipenv): library management
* [FastAPI](https://github.com/tiangolo/fastapi): easy webservice (this includes much more!)

## External links
<https://scipbook.readthedocs.io/en/latest/bpp.html>
