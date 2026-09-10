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

*Nerd talk*: This is the 2D "Cutting Stock Problem", which is NP-hard.
No algorithm exists to calculate a perfect solution in polynomial time, therefore brute force (perfect
solution) is used for small jobs (usually <12 entries) and FFD (fast solution) for larger ones.
When multiple solutions yield equal total trimmings, the solver deterministically breaks ties by comparing descending offcut sizes. This prioritizes woodworking scrap utility (favoring fewer, larger reusable offcuts over fragmented scraps) and guarantees deterministic execution under Python 3.13 hash randomization.

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

Both `linux/amd64` and `linux/arm64` are currently supported, more will be build whenever I get around to it, message
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

### Git & Releases

Unit tests should be run locally before releasing to save on CI executions!
1. Bump the authoritative version string in `app/settings.py` (`version = "vX.Y.Z"`).
2. Commit your changes and tag manually:
   ```bash
   git tag vX.Y.Z
   git push origin main
   git push origin vX.Y.Z
   ```
GitHub Actions CI will automatically execute the full test suite and build/publish multi-arch Docker images (`linux/amd64,linux/arm64`) to Docker Hub (`modischfabrications/cutsolver:<VERSION>`) and GHCR.
Note: 32-bit ARM (`linux/arm/v7`) is retired.

### Testing

Run the test suite locally using `pipenv`:
```bash
pipenv run pytest
```

- **Import Paths**: Make sure your code and test changes preserve `app.*` package imports.
- **Coverage**: Run with coverage reporting (baseline ~94% on core solver logic):
  ```bash
  pipenv run python -m pytest --durations=5 --cov=app/ --cov-report term-missing
  ```
- **Type Checking**: Run static type verification:
  ```bash
  pipenv run python -m mypy app
  ```

### Docker

Prebuilt multi-arch images (`linux/amd64,linux/arm64`) are published automatically on tag pushes.

To build and run a container locally for development:
```bash
docker run --rm -it -p 8000:80 $(docker build -q .)
```

Docker compose is similar, see included files on how to integrate them into your stack. 

## Dependencies

*Everything should be handled by Docker and/or pipenv.*

This project uses:

* [FastAPI](https://github.com/tiangolo/fastapi): easy API (this includes much more!)
* [Uvicorn](https://github.com/encode/uvicorn): async web server
* [more-itertools](https://github.com/more-itertools/more-itertools): higher performance permutations

Also used for development is:

* [pipenv](https://github.com/pypa/pipenv): library management
* [httpie](https://github.com/jakubroztocil/httpie): simpler `curl` for docker healthchecks
* [pytest](https://pytest.org): A lot nicer unit tests
* [flake8](https://flake8.pycqa.org/): Linting
* [mypy](https://mypy-lang.org/): Static type checking
* [requests](https://requests.readthedocs.io/): simple HTTP requests
* [httpx](https://www.python-httpx.org/): requirement of TestClient
* [black](https://github.com/psf/black): uncompromising code formatter; currently unused

## External links

<https://scipbook.readthedocs.io/en/latest/bpp.html>
