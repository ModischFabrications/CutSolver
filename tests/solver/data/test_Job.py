import pytest

from app.solver.data.Job import Job
from app.solver.data.Job import TargetSize
from tests.test_fixtures import testjob_s


def test_iterator(testjob_s):
    job: Job = testjob_s

    resulting_list = []
    for length in job.iterate_sizes():
        resulting_list.append(length)

    assert resulting_list == [
        (500, "Part1"),
        (500, "Part1"),
        (200, "Part2"),
        (200, "Part2"),
        (200, "Part2"),
        (200, "Part2"),
    ]


def test_job_equal(testjob_s):
    job1 = testjob_s
    job2 = testjob_s

    assert job1 == job2


def test_job_length(testjob_s):
    job1 = testjob_s

    assert job1.n_targets() == 6


def test_job_combinations(testjob_s):
    job1 = testjob_s

    assert job1.n_combinations() == 15


def test_equal_hash(testjob_s):
    job1 = testjob_s
    job2 = testjob_s

    assert hash(job1) == hash(job2)


def test_valid(testjob_s):
    job1 = testjob_s
    job1.assert_valid()


def test_invalid(testjob_s):
    invalid_job = testjob_s
    with pytest.raises(ValueError):
        invalid_job.max_length = -1

    with pytest.raises(ValueError):
        invalid_job.cut_width = -1


def test_too_long(testjob_s):
    with pytest.raises(ValueError):
        job = Job(
            max_length=100,
            cut_width=5,
            target_sizes=(TargetSize(length=101, quantity=1),)
        )


def test_to_json():
    job = Job(
        max_length=1200,
        cut_width=5,
        target_sizes=[
            TargetSize(length=300, quantity=4, name="Part1"),
            TargetSize(length=200, quantity=3),
        ],
    )
    assert (
            job.model_dump_json()
            == '{"max_length":1200,"cut_width":5,"target_sizes":[{"length":300,"quantity":4,"name":"Part1"},{"length":200,"quantity":3,"name":""}]}'
    )
