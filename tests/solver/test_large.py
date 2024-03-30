from app.solver.data.Job import TargetSize
from app.solver.solver import (
    _solve_bruteforce,
    _solve_FFD, _solve_gapfill, )
from app.solver.utils import _get_trimmings
from tests.test_fixtures import *


# close to the max for bruteforce!
@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_m(solver):
    testjob_m = Job(max_length=1000, cut_width=5, target_sizes=(
        TargetSize(length=500, quantity=4), TargetSize(length=300, quantity=3),
        TargetSize(length=100, quantity=2)))

    solved = solver(testjob_m)

    assert solved == (
        ((500, ''), (300, ''), (100, '')),
        ((500, ''), (300, ''), (100, '')),
        ((500, ''), (300, '')),
        ((500, ''),))


@pytest.mark.parametrize("solver", [_solve_FFD, _solve_gapfill])
def test_l(solver):
    testjob_l = Job(max_length=2000, cut_width=5, target_sizes=(
        TargetSize(length=750, quantity=5), TargetSize(length=500, quantity=5),
        TargetSize(length=300, quantity=10), TargetSize(length=100, quantity=15)))

    solved = solver(testjob_l)

    assert solved == (
        ((300, ''), (100, ''), (100, ''), (100, ''), (100, ''), (100, ''), (100, ''), (100, ''), (100, ''), (100, '')),
        ((300, ''), (300, ''), (300, ''), (300, ''), (300, ''), (300, ''), (100, '')),
        ((750, ''), (500, ''), (500, ''), (100, ''), (100, '')),
        ((500, ''), (500, ''), (500, ''), (300, ''), (100, '')),
        ((750, ''), (750, ''), (300, ''), (100, '')),
        ((750, ''), (750, ''), (300, ''), (100, '')))


# tests after here are only benchmarking and shouldn't ever be relevant

@pytest.mark.parametrize("solver", [_solve_FFD, _solve_gapfill])
def test_xl(solver):
    testjob = Job(max_length=2000, cut_width=10, target_sizes=(
        TargetSize(length=2000, quantity=5), TargetSize(length=1500, quantity=10),
        TargetSize(length=750, quantity=25), TargetSize(length=500, quantity=50),
        TargetSize(length=300, quantity=100), TargetSize(length=50, quantity=250),
    ))

    solved = solver(testjob)

    assert _get_trimmings(testjob.max_length, solved, testjob.cut_width) == 2520


@pytest.mark.parametrize("solver", [_solve_FFD, _solve_gapfill])
def test_xxl(solver):
    testjob = Job(max_length=2000, cut_width=10, target_sizes=(
        TargetSize(length=1750, quantity=5), TargetSize(length=1500, quantity=10),
        TargetSize(length=750, quantity=25), TargetSize(length=500, quantity=50),
        TargetSize(length=300, quantity=100), TargetSize(length=200, quantity=150),
        TargetSize(length=150, quantity=250), TargetSize(length=50, quantity=500),
    ))

    solved = solver(testjob)

    assert _get_trimmings(testjob.max_length, solved, testjob.cut_width) == 3250
