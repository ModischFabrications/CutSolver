from pathlib import Path

import pytest

from app.solver.data.Job import Job
from app.solver.data.Result import Result


def load_json(json_path: Path):
    assert json_path.exists()

    with json_path.open("r") as encoded_obj:
        return encoded_obj.read()


@pytest.fixture
def testjob_s():
    return Job.model_validate_json(load_json(Path("./tests/res/in/testjob_s.json")))


@pytest.fixture
def testresult_s():
    return Result.model_validate_json(
        load_json(Path("./tests/res/out/testresult_s.json"))
    )


@pytest.fixture
def testjob_m():
    return Job.model_validate_json(load_json(Path("./tests/res/in/testjob_m.json")))


@pytest.fixture
def testjob_l():
    return Job.model_validate_json(load_json(Path("./tests/res/in/testjob_l.json")))


@pytest.fixture
def testjob_cuts():
    return Job.model_validate_json(load_json(Path("./tests/res/in/testjob_cuts.json")))


@pytest.fixture
def testjob_zero_cuts():
    return Job.model_validate_json(load_json(Path("./tests/res/in/testjob_zero_cuts.json")))


@pytest.fixture
def testjob_equal():
    return Job.model_validate_json(load_json(Path("./tests/res/in/testjob_equal.json")))
