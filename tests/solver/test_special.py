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
def test_zero_cuts(solver):
    testjob_zero_cuts = Job(stocks=(INS(length=1000),), cut_width=0, required=(QNS(length=500, quantity=4),))
    solved = solver(testjob_zero_cuts)

    assert solved == (
        ResultEntry(stock=NS(length=1000), cuts=(NS(length=500), NS(length=500)), trimming=0),
        ResultEntry(stock=NS(length=1000), cuts=(NS(length=500), NS(length=500)), trimming=0)
    )


# @pytest.mark.skip(reason="bug #64")
@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_equal(solver):
    testjob_equal = Job(stocks=(INS(length=1000),), cut_width=10, required=(QNS(length=1000, quantity=4),))
    solved = solver(testjob_equal)

    assert solved == (
        ResultEntry(stock=NS(length=1000), cuts=(NS(length=1000),), trimming=0),
        ResultEntry(stock=NS(length=1000), cuts=(NS(length=1000),), trimming=0),
        ResultEntry(stock=NS(length=1000), cuts=(NS(length=1000),), trimming=0),
        ResultEntry(stock=NS(length=1000), cuts=(NS(length=1000),), trimming=0)
    )
