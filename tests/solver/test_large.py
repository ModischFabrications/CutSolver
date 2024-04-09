from app.solver.data.Job import TS, StockSize, NS
from app.solver.solver import (
    _solve_bruteforce,
    _solve_FFD, _solve_gapfill, )
from tests.test_fixtures import *


# close to the max for bruteforce!
@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_m(solver):
    testjob_m = Job(stocks=(StockSize(length=1000),), cut_width=5, required=(
        TS(length=500, quantity=4), TS(length=300, quantity=3),
        TS(length=100, quantity=2)))

    solved = solver(testjob_m)

    # I don't care about ordering here
    assert sorted([r.cuts for r in solved]) == sorted([
        (NS(length=500), NS(length=300), NS(length=100)),
        (NS(length=500), NS(length=300), NS(length=100)),
        (NS(length=500), NS(length=300)),
        (NS(length=500),)
    ])


@pytest.mark.parametrize("solver", [_solve_FFD, _solve_gapfill])
def test_l(solver):
    testjob_l = Job(stocks=(StockSize(length=2000),), cut_width=5, required=(
        TS(length=750, quantity=5), TS(length=500, quantity=5),
        TS(length=300, quantity=10), TS(length=100, quantity=15)))

    solved = solver(testjob_l)

    # I don't care about ordering here
    assert sorted([r.cuts for r in solved]) == sorted([
        (NS(length=300), NS(length=100), NS(length=100), NS(length=100),
         NS(length=100), NS(length=100), NS(length=100), NS(length=100),
         NS(length=100), NS(length=100)),
        (NS(length=300), NS(length=300), NS(length=300), NS(length=300),
         NS(length=300), NS(length=300), NS(length=100)),
        (NS(length=750), NS(length=500), NS(length=500), NS(length=100),
         NS(length=100)),
        (NS(length=500), NS(length=500), NS(length=500), NS(length=300),
         NS(length=100)),
        (NS(length=750), NS(length=750), NS(length=300), NS(length=100)),
        (NS(length=750), NS(length=750), NS(length=300), NS(length=100))
    ])


# tests after here are only benchmarking and shouldn't ever be relevant

@pytest.mark.parametrize("solver", [_solve_FFD, _solve_gapfill])
def test_xl(solver):
    testjob = Job(stocks=(StockSize(length=2000),), cut_width=10, required=(
        TS(length=2000, quantity=5), TS(length=1500, quantity=10),
        TS(length=750, quantity=25), TS(length=500, quantity=50),
        TS(length=300, quantity=100), TS(length=50, quantity=250),
    ))

    solved = solver(testjob)

    assert sum(l.trimming for l in solved) == 2520


@pytest.mark.parametrize("solver", [_solve_FFD, _solve_gapfill])
def test_xxl(solver):
    testjob = Job(stocks=(StockSize(length=2000),), cut_width=10, required=(
        TS(length=1750, quantity=5), TS(length=1500, quantity=10),
        TS(length=750, quantity=25), TS(length=500, quantity=50),
        TS(length=300, quantity=100), TS(length=200, quantity=150),
        TS(length=150, quantity=250), TS(length=50, quantity=500),
    ))

    solved = solver(testjob)

    assert sum(l.trimming for l in solved) == 3250
