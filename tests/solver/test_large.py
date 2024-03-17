from app.solver.solver import (
    _solve_bruteforce,
    _solve_FFD,
)
from tests.test_fixtures import *


# close to the max for bruteforce!
@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD])
def test_m(testjob_m, solver):
    orig_job = testjob_m.model_copy(deep=True)
    solved = solver(testjob_m)

    assert solved == [[(500, '')],
                      [(500, ''), (300, '')],
                      [(500, ''), (300, '')],
                      [(500, ''), (300, ''), (100, '')]]
    assert orig_job == testjob_m


@pytest.mark.parametrize("solver", [_solve_FFD])
def test_l(testjob_l, solver):
    orig_job = testjob_l.model_copy(deep=True)
    solved = solver(testjob_l)

    assert solved == [[(750, ''), (750, ''), (300, ''), (100, '')],
                      [(750, ''), (750, ''), (300, ''), (100, '')],
                      [(750, ''), (500, ''), (500, ''), (100, ''), (100, '')],
                      [(500, ''), (500, ''), (500, ''), (300, ''), (100, '')],
                      [(300, ''), (300, ''), (300, ''), (300, ''), (300, ''), (300, ''), (100, '')],
                      [(300, ''), (100, ''), (100, ''), (100, ''), (100, ''), (100, ''), (100, ''), (100, ''),
                       (100, ''), (100, '')]]
    assert orig_job == testjob_l
