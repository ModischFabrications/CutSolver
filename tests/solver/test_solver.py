from pathlib import Path

import pytest

from app.solver.data.Job import QNS, Job, INS
from app.solver.data.Result import SolverType, Result
from app.solver.solver import (
    _solve_bruteforce,
    _solve_gapfill,
    _solve_FFD, solve,
)
from tests.conftest import load_json


@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_solver_is_optimal(testjob_s, solver):
    solved = solver(testjob_s)

    assert sum(lt.trimming for lt in solved) == 1188


@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_solver_is_exactly(testjob_s, solver):
    orig_job = testjob_s.model_copy(deep=True)

    assert orig_job == testjob_s


@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_solver_no_side_effects(testjob_s, solver):
    orig_job = testjob_s.model_copy(deep=True)
    _ = solver(testjob_s)

    assert orig_job == testjob_s


def test_distribute():
    testjob = Job(stocks=(INS(length=1010),), cut_width=10,
                  required=(QNS(length=500, quantity=8), QNS(length=500, quantity=4)))
    solved = solve(testjob)

    assert solved.solver_type == SolverType.bruteforce

    testjob = Job(stocks=(INS(length=1010),), cut_width=10, required=(
        QNS(length=250, quantity=50), QNS(length=500, quantity=50)))
    solved = solve(testjob)

    assert solved.solver_type == SolverType.FFD


def test_distribute_too_large():
    testjob = Job(stocks=(INS(length=1010),), cut_width=10, required=(
        QNS(length=250, quantity=2000), QNS(length=500, quantity=500)))

    with pytest.raises(OverflowError):
        _ = solve(testjob)


def test_full_solver():
    job = Job.model_validate_json(load_json(Path("./tests/res/in/testjob_s.json")))
    solved = solve(job)
    encoded_solved = solved.model_dump_json(exclude_defaults=True)

    assert len(encoded_solved) > 20

    result = Result.model_validate_json(load_json(Path("./tests/res/out/testresult_s.json")))

    assert solved.job == job
    assert solved == result
