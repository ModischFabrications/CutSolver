import pytest

from app.solver.data.Job import Job, INS, NS
from app.solver.data.Job import QNS
from tests.test_fixtures import testjob_s


def test_constructor():
    job = Job(stocks=(INS(length=1010),), cut_width=10, required=(QNS(length=500, quantity=4),))
    assert job


def test_iterator(testjob_s):
    resulting_list = []
    for length in testjob_s.iterate_required():
        resulting_list.append(length)

    assert resulting_list == [
        NS(length=500, name='Part1'),
        NS(length=500, name='Part1'),
        NS(length=200, name='Part2'),
        NS(length=200, name='Part2'),
        NS(length=200, name='Part2'),
        NS(length=200, name='Part2')
    ]


def test_job_equal(testjob_s):
    job1 = testjob_s
    job2 = testjob_s

    assert job1 == job2


def test_job_length(testjob_s):
    job = testjob_s

    assert job.n_targets() == 6


def test_job_combinations(testjob_s):
    job = testjob_s

    assert job.n_combinations() == 15


def test_equal_hash(testjob_s):
    job1 = testjob_s
    job2 = testjob_s

    assert hash(job1) == hash(job2)


def test_invalid(testjob_s):
    invalid_job = testjob_s

    with pytest.raises(ValueError):
        invalid_job.cut_width = -1

    with pytest.raises(ValueError):
        invalid_job.stocks = invalid_job.required


def test_too_long(testjob_s):
    with pytest.raises(ValueError):
        _ = Job(
            max_length=100,
            cut_width=5,
            required=(QNS(length=101, quantity=1),)
        )


def test_solver_multi_overflow():
    with pytest.raises(ValueError):
        _ = Job(stocks=(INS(length=1100, quantity=1), INS(length=500, quantity=1)), cut_width=10,
                required=(QNS(length=500, quantity=2), QNS(length=1000, quantity=2)))


def test_to_json():
    job = Job(
        stocks=(INS(length=1200),),
        cut_width=5,
        required=[
            QNS(length=300, quantity=4, name="Part1"),
            QNS(length=200, quantity=3),
        ],
    )
    assert (
            job.model_dump_json(exclude_defaults=True)
            == '{"cut_width":5,"stocks":[{"length":1200}],"required":[{"length":300,"name":"Part1","quantity":4},'
               '{"length":200,"quantity":3}]}'
    )
