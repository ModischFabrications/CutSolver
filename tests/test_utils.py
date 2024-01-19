from pathlib import Path

from app.solver.data.Job import Job
from app.solver.data.Result import Result


def load_json(json_path: Path):
    assert json_path.exists()

    with json_path.open("r") as encoded_obj:
        return encoded_obj.read()


def generate_testjob():
    return Job.model_validate_json(load_json(Path("./tests/res/in/testjob.json")))


def generate_testresult():
    return Result.model_validate_json(
        load_json(Path("./tests/res/out/testresult.json"))
    )
