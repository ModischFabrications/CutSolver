from fastapi import FastAPI

from app.model.CutSolver import distribute
from app.model.Job import JobSchema, Job, ResultSchema

app = FastAPI()


@app.post("/solve")
def solve(job: str):
    job = JobSchema().loads(job).data
    assert job.__class__ == Job

    print(f"Got job with ID {job.get_ID()}")

    solved = distribute(job)

    return ResultSchema().dumps(solved).data


@app.get("/")
def index():
    # TODO: add index and hyperlinks
    return f"Hello FastAPI!\n"


@app.get("/about")
def about():
    text = 'Visit <a href="https://github.com/ModischFabrications/CutSolver">' \
           'the repository</a> for further informations.'
    return text
