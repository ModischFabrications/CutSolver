import platform

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, PlainTextResponse

# don't mark /app as a sources root or pycharm will delete the "app." prefix
# that's needed for pytest to work correctly
from app.solver.data.Job import Job
from app.solver.data.Result import Result
from app.solver.solver import distribute

version = "v0.4.6"

app = FastAPI(
    title="CutSolverBackend",
    version=version
)


# needs to be before CORS!
# https://github.com/tiangolo/fastapi/issues/775#issuecomment-592946834
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # TODO: filter out expected exceptions and let unexpected ones go?
        # probably want some kind of logging here
        return PlainTextResponse(str(e), status_code=400)


app.middleware("http")(catch_exceptions_middleware)

cors_origins = [
    "http:localhost",
    "https:localhost",
    "http:localhost:8080",
    "*",  # this might be dangerous
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# response model ensures correct documentation
@app.post("/solve", response_model=Result)
def post_solve(job: Job):
    # pydantic guarantees type safety
    job.assert_valid()

    solved: Result = distribute(job)
    solved.assert_valid()

    return solved


@app.get("/debug", response_class=HTMLResponse)
def get_debug():
    static_answer = (
        "Debug Infos:"
        "<ul>"
        f"<li>Node: {platform.node()}</li>"
        f"<li>System: {platform.system()}</li>"
        f"<li>Architecture: {platform.machine()}</li>"
        f"<li>Python Version: {platform.python_version()}</li>"
        f"<li>Python Impl: {platform.python_implementation()}</li>"
    )

    return static_answer


# content_type results in browser pretty printing
@app.get("/", response_class=HTMLResponse)
def get_root():
    static_answer = (
        f"<h2>Hello from CutSolver {version}!</h2>"
        '<h3>Have a look at the documentation at <a href="/docs">/docs</a> for usage hints.</h3>'
        'Visit <a href="https://github.com/ModischFabrications/CutSolver">the repository</a> for further information. '
        'Debug stuff is available at <a href="/debug">/debug</a>. '
    )

    return static_answer


@app.get("/version", response_class=PlainTextResponse)
def get_version():
    return version


# for debugging only
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
