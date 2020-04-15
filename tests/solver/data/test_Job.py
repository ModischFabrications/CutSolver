import pytest

from tests.test_utils import generate_testjob


def test_iterator():
    job = generate_testjob()

    resulting_list = []
    for length in job.iterate_sizes():
        resulting_list.append(length)

    assert resulting_list == [500, 500, 200, 200, 200, 200]


def test_job_equal():
    job1 = generate_testjob()
    job2 = generate_testjob()

    assert job1 == job2


def test_job_length():
    job1 = generate_testjob()

    assert len(job1) == 6


def test_equal_hash():
    job1 = generate_testjob()
    job2 = generate_testjob()

    assert hash(job1) == hash(job2)


def test_valid():
    job1 = generate_testjob()
    job1.assert_valid()


def test_invalid():
    invalid_job = generate_testjob()
    invalid_job.max_length = -1
    with pytest.raises(ValueError):
        invalid_job.assert_valid()


def test_too_long():
    job = generate_testjob()
    job.target_sizes[job.max_length + 1] = 4
    with pytest.raises(ValueError):
        job.assert_valid()
