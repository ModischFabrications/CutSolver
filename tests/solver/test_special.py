import pytest

from app.solver.data.Job import QNS, Job, INS, NS
from app.solver.data.Result import ResultEntry
from app.solver.solver import (
    _solve_bruteforce,
    _solve_FFD, _solve_gapfill,
)


# @pytest.mark.skip(reason="bug #63")
@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_cuts(solver):
    testjob_cuts = Job(stocks=(INS(length=1010),), cut_width=10, required=(QNS(length=500, quantity=4),))
    solved = solver(testjob_cuts)

    assert solved == (
        ResultEntry(stock=NS(length=1010), cuts=(NS(length=500), NS(length=500)), trimming=0),
        ResultEntry(stock=NS(length=1010), cuts=(NS(length=500), NS(length=500)), trimming=0)
    )


# @pytest.mark.skip(reason="bug #59")
@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_zero_width_cuts(solver):
    testjob_zero_cuts = Job(stocks=(INS(length=1000),), cut_width=0, required=(QNS(length=500, quantity=4),))
    solved = solver(testjob_zero_cuts)

    assert solved == (
        ResultEntry(stock=NS(length=1000), cuts=(NS(length=500), NS(length=500)), trimming=0),
        ResultEntry(stock=NS(length=1000), cuts=(NS(length=500), NS(length=500)), trimming=0)
    )


@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_smaller_cuts(solver):
    testjob = Job(
        stocks=(INS(length=100),),
        cut_width=10,
        required=(QNS(length=95, quantity=2),)
    )

    solved = solver(testjob)

    assert solved == (
        ResultEntry(stock=NS(length=100), cuts=(NS(length=95),), trimming=0),
        ResultEntry(stock=NS(length=100), cuts=(NS(length=95),), trimming=0))


# @pytest.mark.skip(reason="bug #64")
@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_no_cuts(solver):
    testjob_equal = Job(stocks=(INS(length=1000),), cut_width=10, required=(QNS(length=1000, quantity=4),))
    solved = solver(testjob_equal)

    assert solved == (
        ResultEntry(stock=NS(length=1000), cuts=(NS(length=1000),), trimming=0),
        ResultEntry(stock=NS(length=1000), cuts=(NS(length=1000),), trimming=0),
        ResultEntry(stock=NS(length=1000), cuts=(NS(length=1000),), trimming=0),
        ResultEntry(stock=NS(length=1000), cuts=(NS(length=1000),), trimming=0)
    )


@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_infinite_stocks(solver):
    testjob_q = Job(stocks=(INS(length=100, quantity=10),), cut_width=5, required=(QNS(length=100, quantity=2),))
    testjob_i = Job(stocks=(INS(length=100),), cut_width=5, required=(QNS(length=100, quantity=2),))

    solved_q = solver(testjob_q)
    solved_i = solver(testjob_i)

    assert solved_q == solved_i
    assert solved_q == (ResultEntry(stock=NS(length=100), cuts=(NS(length=100),), trimming=0),
                        ResultEntry(stock=NS(length=100), cuts=(NS(length=100),), trimming=0))


@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_ignore_stocks(solver):
    testjob = Job(
        stocks=(INS(length=1000), INS(length=99, quantity=5)),
        cut_width=5,
        required=(QNS(length=500, quantity=4), QNS(length=100, quantity=2))
    )

    solved = solver(testjob)

    assert solved == (
        ResultEntry(stock=NS(length=1000), cuts=(NS(length=500), NS(length=100), NS(length=100)), trimming=285),
        ResultEntry(stock=NS(length=1000), cuts=(NS(length=500),), trimming=495),
        ResultEntry(stock=NS(length=1000), cuts=(NS(length=500),), trimming=495),
        ResultEntry(stock=NS(length=1000), cuts=(NS(length=500),), trimming=495)
    )


@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_big_and_small(solver):
    testjob = Job(
        stocks=(INS(length=1000), INS(length=100)),
        cut_width=10,
        required=(QNS(length=100, quantity=2), QNS(length=1000, quantity=1))
    )

    solved = solver(testjob)

    assert solved == (
        ResultEntry(stock=NS(length=100), cuts=(NS(length=100),), trimming=0),
        ResultEntry(stock=NS(length=100), cuts=(NS(length=100),), trimming=0),
        ResultEntry(stock=NS(length=1000), cuts=(NS(length=1000),), trimming=0))


@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_close_stocks(solver):
    testjob = Job(
        stocks=(INS(length=500), INS(length=100)),
        cut_width=5,
        required=(QNS(length=100, quantity=4),)
    )

    solved = solver(testjob)

    assert solved == (
        ResultEntry(stock=NS(length=100), cuts=(NS(length=100),), trimming=0),
        ResultEntry(stock=NS(length=100), cuts=(NS(length=100),), trimming=0),
        ResultEntry(stock=NS(length=100), cuts=(NS(length=100),), trimming=0),
        ResultEntry(stock=NS(length=100), cuts=(NS(length=100),), trimming=0))
