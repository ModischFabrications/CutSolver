import platform

from fastapi import FastAPI
from starlette.responses import HTMLResponse

from app.model.CutSolver import distribute
from app.model.Job import Job
from app.model.Result import Result

app = FastAPI()


# response model ensures correct documentation
@app.post("/solve", response_model=Result)
def solve(job: Job):
    assert job.__class__ == Job

    solved = distribute(job)

    return solved


@app.get("/debug", response_class=HTMLResponse)
def debug_info():
    static_answer = f"Debug Infos:" \
        f"<ul>" \
        f"<li>System: {platform.system()}</li>" \
        f"<li>Architecture: {platform.machine()}</li>" \
        f"<li>Python Version: {platform.python_version()}</li>" \
        f"<li>Python Impl: {platform.python_implementation()}</li>"

    return static_answer


# content_type results in browser pretty printing
@app.get("/", response_class=HTMLResponse)
def index():
    static_answer = f"<h2>Hello from {platform.node()}!</h2>" \
        f"<h3>Have a look at the documentation at <a href=\"/docs\">/docs</a> for usage hints.</h3>" \
        f"Debug information are at <a href=\"/debug\">/debug</a>"

    return static_answer


@app.get("/about", response_class=HTMLResponse)
def about():
    text = 'Visit <a href="https://github.com/ModischFabrications/CutSolver">' \
           'the repository</a> for further informations.'
    return text


# for debugging only
if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
