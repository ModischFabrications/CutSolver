from fastapi import FastAPI
from starlette.responses import HTMLResponse

from app.model.CutSolver import distribute
from app.model.Job import Job, Result

app = FastAPI()


# response model ensures correct documentation
@app.post("/solve", response_model=Result)
def solve(job: Job):
    assert job.__class__ == Job

    solved = distribute(job)

    return solved


# content_type results in browser pretty printing
@app.get("/", response_class=HTMLResponse)
def index():
    # TODO: redirect to docs
    return "Hello FastAPI!"


@app.get("/about", response_class=HTMLResponse)
def about():
    text = 'Visit <a href="https://github.com/ModischFabrications/CutSolver">' \
           'the repository</a> for further informations.'
    return text


# for debugging only
if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
