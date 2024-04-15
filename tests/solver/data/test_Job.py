import pytest
from pydantic import ValidationError

from app.solver.data.Job import Job, INS, NS
from app.solver.data.Job import QNS


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

    assert job.n_entries() == 6


def test_combinations_required():
    # check with len(list(distinct_permutations(job.iterate_required())))
    # TODO maybe generate a whole list of jobs to check against automatically?

    job = Job(stocks=(INS(length=1000),), cut_width=10, required=(
        QNS(length=88, quantity=1),))
    assert job.n_combinations_required() == 1

    job = Job(stocks=(INS(length=1000),), cut_width=10, required=(
        QNS(length=88, quantity=2), QNS(length=77, quantity=1)))
    assert job.n_combinations_required() == 3

    job = Job(stocks=(INS(length=1000),), cut_width=10, required=(
        QNS(length=99, quantity=3), QNS(length=88, quantity=2), QNS(length=77, quantity=1)))
    assert job.n_combinations_required() == 60


def test_combinations_stocks():
    job = Job(stocks=(INS(length=1000, quantity=1),), cut_width=10, required=(
        QNS(length=88, quantity=1),))
    assert job.n_combinations_stocks() == 1

    job = Job(stocks=(INS(length=1000, quantity=2), INS(length=900, quantity=1)), cut_width=10, required=(
        QNS(length=88, quantity=2),))
    assert job.n_combinations_stocks() == 3


def test_combinations():
    # infinites can't really be tested, but are always larger than needed anyway
    job = Job(stocks=(INS(length=1000, quantity=2),), cut_width=10, required=(QNS(length=99, quantity=4),))
    assert job.n_combinations() == 1

    job = Job(stocks=(INS(length=1000, quantity=2), INS(length=100, quantity=2)), cut_width=10, required=(
        QNS(length=500, quantity=2), QNS(length=300, quantity=1), QNS(length=100, quantity=1))
              )
    assert job.n_combinations() == 72

    # TODO test combined once grouping works


@pytest.mark.xfail(reason="bug #73")
def test_group_required():
    job = Job(stocks=(INS(length=1000),), cut_width=10, required=(
        QNS(length=88, quantity=2), QNS(length=88, quantity=1), QNS(length=88, quantity=1))
              )
    assert job.n_combinations_required() == 1


@pytest.mark.xfail(reason="bug #73")
def test_group_stocks():
    job = Job(stocks=(INS(length=1000, quantity=2), INS(length=1000, quantity=2)), cut_width=10,
              required=(QNS(length=100, quantity=2),))
    assert job.n_combinations_stocks() == 1


@pytest.mark.xfail(reason="bug #73")
def test_group_stocks_infinite():
    job = Job(stocks=(INS(length=1000, quantity=2), INS(length=1000)), cut_width=10,
              required=(QNS(length=100, quantity=2),))
    assert job.n_combinations_stocks() == 1


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
    with pytest.raises(ValidationError, match='target sizes longer than the stock'):
        _ = Job(
            stocks=(INS(length=100),),
            cut_width=5,
            required=(QNS(length=101, quantity=1),)
        )


def test_too_long_multi(testjob_s):
    with pytest.raises(ValidationError, match='target sizes longer than the stock'):
        _ = Job(stocks=(INS(length=100, quantity=100), INS(length=500)), cut_width=10,
                required=(QNS(length=500, quantity=2), QNS(length=1000, quantity=2)))


def test_solver_multi_overflow():
    with pytest.raises(ValueError, match='more targets than the stock available'):
        _ = Job(stocks=(INS(length=1100, quantity=1), INS(length=500, quantity=1)), cut_width=10,
                required=(QNS(length=500, quantity=2), QNS(length=1000, quantity=2)))


def test_solver_skip_too_short():
    job = Job(stocks=(INS(length=100, quantity=10), INS(length=1000)), cut_width=10,
              required=(QNS(length=500, quantity=2), QNS(length=1000, quantity=2)))

    assert not any(stock.length != 1000 for stock in job.iterate_stocks())


def test_infinite_count():
    job = Job(
        stocks=(INS(length=100),),
        cut_width=1,
        required=(QNS(length=50, quantity=6),)
    )

    assert len(list(job.iterate_stocks())) >= 6


def test_to_json():
    job = Job(
        stocks=(INS(length=1200),),
        cut_width=5,
        required=(
            QNS(length=300, quantity=4, name="Part1"),
            QNS(length=200, quantity=3),
        ),
    )
    assert (
            job.model_dump_json(exclude_defaults=True)
            == '{"cut_width":5,"stocks":[{"length":1200}],"required":[{"length":300,"name":"Part1","quantity":4},'
               '{"length":200,"quantity":3}]}'
    )
