from app.solver.data.Job import TargetSize
from app.solver.solver import (
    _solve_bruteforce,
    _solve_FFD, _solve_gapfill,
)
from tests.test_fixtures import *


# @pytest.mark.skip(reason="bug #63")
@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_cuts(solver):
    testjob_cuts = Job(max_length=1010, cut_width=10, target_sizes=(TargetSize(length=500, quantity=4),))
    solved = solver(testjob_cuts)

    assert solved == (
        ((500, ''), (500, '')),
        ((500, ''), (500, ''))
    )


@pytest.mark.skip(reason="bug #59")
@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_zero_cuts(solver):
    testjob_zero_cuts = Job(max_length=1000, cut_width=0, target_sizes=(TargetSize(length=500, quantity=4),))
    solved = solver(testjob_zero_cuts)

    assert solved == (
        ((500, ''), (500, '')),
        ((500, ''), (500, ''))
    )


# @pytest.mark.skip(reason="bug #64")
@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_equal(solver):
    testjob_equal = Job(max_length=1000, cut_width=10, target_sizes=(TargetSize(length=1000, quantity=4),))
    solved = solver(testjob_equal)

    assert solved == (
        ((1000, ''),),
        ((1000, ''),),
        ((1000, ''),),
        ((1000, ''),)
    )
