from fastapi import FastAPI

from model.CutSolver import distribute
from model.Job import Job

app = FastAPI()


@app.post("/solve")
def solve(job: Job):
    assert job.__class__ == Job

    print(f"Got job with length {len(job)}")

    solved = distribute(job)

    return solved


@app.get("/")
def index():
    # TODO: redirect to docs
    return "Hello FastAPI!"


@app.get("/about")
def about():
    text = 'Visit <a href="https://github.com/ModischFabrications/CutSolver">' \
           'the repository</a> for further informations.'
    return text
