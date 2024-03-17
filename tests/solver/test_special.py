from app.solver.solver import (
    _solve_bruteforce,
    _solve_FFD,
)
from tests.test_fixtures import *


@pytest.mark.skip(reason="bug #63")
@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD])
def test_cuts(testjob_cuts, solver):
    orig_job = testjob_cuts.model_copy(deep=True)
    solved = solver(testjob_cuts)

    assert solved == [
        [(500, ''), (500, '')],
        [(500, ''), (500, '')]
    ]
    assert orig_job == testjob_cuts


@pytest.mark.skip(reason="bug #59")
@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD])
def test_zero_cuts(testjob_zero_cuts, solver):
    orig_job = testjob_zero_cuts.model_copy(deep=True)
    solved = solver(testjob_zero_cuts)

    assert solved == [
        [(500, ''), (500, '')],
        [(500, ''), (500, '')]
    ]
    assert orig_job == testjob_zero_cuts


@pytest.mark.skip(reason="bug #64")
@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD])
def test_equal(testjob_equal, solver):
    orig_job = testjob_equal.model_copy(deep=True)
    solved = solver(testjob_equal)

    assert solved == [
        [(1000, '')],
        [(1000, '')],
        [(1000, '')],
        [(1000, '')]
    ]
    assert orig_job == testjob_equal
