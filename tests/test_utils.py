from pathlib import Path

from app.solver.data.Job import Job
from app.solver.data.Result import Result


def generate_testjob():
    json_job = Path("./tests/res/in/testjob.json")
    assert json_job.exists()

    with open(json_job, "r") as encoded_job:
        return Job.parse_raw(encoded_job.read())


def generate_testresult():
    json_result = Path("./tests/res/out/testresult.json")
    assert json_result.exists()

    with open(json_result, "r") as encoded_result:
        return Result.parse_raw(encoded_result.read())
