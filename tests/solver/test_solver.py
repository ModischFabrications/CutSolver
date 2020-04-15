from pathlib import Path

import pytest

from solver.CutSolver import _get_trimming, _solve_bruteforce, _solve_gapfill, _solve_FFD, distribute
from solver.data.Job import Job
from solver.data.Result import Result
from tests.test_utils import generate_testjob


def test_trimmings():
    trimming = _get_trimming(max_length=1500, lengths=(300, 400, 600, 100), cut_width=2)

    assert trimming == 92


def test_trimmings_raise():
    # raises Error if more stock was used than available
    with pytest.raises(OverflowError):
        trimming = _get_trimming(1500, (300, 400, 600, 200), 2)


def generate_testjob():
    json_job = Path("./tests/data/in/testjob.json")
    assert json_job.exists()

    with open(json_job, "r") as encoded_job:
        return Job.parse_raw(encoded_job.read())


def test_bruteforce():
    job = generate_testjob()

    cmp_job = job.copy(deep=True)
    solved = _solve_bruteforce(job)

    assert solved.solver_type == "bruteforce"
    assert cmp_job == job


def test_gapfill():
    job = generate_testjob()

    cmp_job = job.copy(deep=True)
    solved = _solve_gapfill(job)

    assert solved.solver_type == "gapfill"
    assert cmp_job == job


def test_FFD():
    job = generate_testjob()

    cmp_job = job.copy(deep=True)
    solved = _solve_FFD(job)

    assert solved.solver_type == "FFD"
    assert cmp_job == job


def test_full_model():
    json_job = Path("./tests/res/in/testjob.json")
    assert json_job.exists()

    json_result = Path("./tests/res/out/testresult.json")

    with open(json_job, "r") as encoded_job:
        job = Job.parse_raw(encoded_job.read())

        solved = distribute(job)

        encoded_solved = solved.json()
        assert len(encoded_solved) > 20

    with open(json_result, "r") as encoded_result:
        result = Result.parse_raw(encoded_result.read())

        assert solved == result
