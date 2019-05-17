from pathlib import Path

import pytest

from app.model.CutSolver import _get_trimming, _solve_bruteforce, _solve_gapfill, _solve_FFD
from app.model.Job import TargetSize, Job


def test_trimmings():
    trimming = _get_trimming(length_stock=1500, lengths=(300, 400, 600, 100), cut_width=2)

    assert trimming == 92


def test_trimmings_raise():
    # raises Error if more stock was used than available
    with pytest.raises(OverflowError):
        trimming = _get_trimming(1500, (300, 400, 600, 200), 2)


def generate_testjob():
    return Job(length_stock=900, target_sizes=(
        TargetSize(length=500, amount=2), TargetSize(length=200, amount=3), TargetSize(length=100, amount=2)),
               cut_width=0)


def test_bruteforce():
    job = generate_testjob()

    cmp_job = job.copy(deep=True)
    solved = _solve_bruteforce(job)

    assert solved.solver == "bruteforce"
    assert cmp_job == job


def test_gapfill():
    job = generate_testjob()

    cmp_job = job.copy(deep=True)
    solved = _solve_gapfill(job)

    assert solved.solver == "gapfill"
    assert cmp_job == job


def test_FFD():
    job = generate_testjob()

    cmp_job = job.copy(deep=True)
    solved = _solve_FFD(job)

    assert solved.solver == "FFD"
    assert cmp_job == job


def test_job_generator():
    job = Job(length_stock=1550, target_sizes=(
        TargetSize(length=500, amount=4), TargetSize(length=200, amount=3), TargetSize(length=100, amount=2)),
              cut_width=5)

    resulting_list = []
    for length in job.get_sizes():
        resulting_list.append(length)

    assert resulting_list == [500, 500, 500, 500, 200, 200, 200, 100, 100]


def test_job_dunders():
    job1 = Job(length_stock=100, target_sizes=(TargetSize(length=100, amount=2), TargetSize(length=200, amount=1)),
               cut_width=0)
    job2 = Job(length_stock=100, target_sizes=(TargetSize(length=100, amount=2), TargetSize(length=200, amount=1)),
               cut_width=0)

    assert job1 == job2
    assert len(job1) == 3


def test_full_model():
    json_file = Path("./tests/testjob.json")
    assert json_file.exists()

    with open(json_file, "r") as encoded_job:
        job = Job.parse_raw(encoded_job.read())

        solved = _solve_gapfill(job)

        encoded_solved = solved.json()
        assert len(encoded_solved) > 20
