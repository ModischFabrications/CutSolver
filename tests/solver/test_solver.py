from app.solver.data.Job import TargetSize
from app.solver.data.Result import SolverType
from app.solver.solver import (
    _solve_bruteforce,
    _solve_gapfill,
    _solve_FFD, solve,
)
from app.solver.utils import _get_trimmings
from tests.test_fixtures import *


@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_solver_is_optimal(testjob_s, solver):
    orig_job = testjob_s.model_copy(deep=True)
    solved = solver(testjob_s)

    assert _get_trimmings(orig_job.max_length, solved, orig_job.cut_width) == 1188
    assert orig_job == testjob_s


@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_solver_is_exactly(testjob_s, solver):
    orig_job = testjob_s.model_copy(deep=True)
    solved = solver(testjob_s)

    assert solved == (
        ((500, "Part1"), (500, "Part1"), (200, "Part2"), (200, "Part2")),
        ((200, "Part2"), (200, "Part2")),
    )
    assert orig_job == testjob_s


def test_distribute():
    testjob = Job(max_length=1010, cut_width=10, target_sizes=(TargetSize(length=500, quantity=4),))
    solved = solve(testjob)

    assert solved.solver_type == SolverType.bruteforce

    testjob = Job(max_length=1010, cut_width=10, target_sizes=(
        TargetSize(length=250, quantity=50), TargetSize(length=500, quantity=50)))
    solved = solve(testjob)

    assert solved.solver_type == SolverType.FFD


def test_distribute_too_large():
    testjob = Job(max_length=1010, cut_width=10, target_sizes=(
        TargetSize(length=250, quantity=2000), TargetSize(length=500, quantity=500)))

    with pytest.raises(OverflowError):
        not_solved = solve(testjob)


def test_full_solver():
    job = Job.model_validate_json(load_json(Path("./tests/res/in/testjob_s.json")))
    solved = solve(job)
    encoded_solved = solved.model_dump_json()

    assert len(encoded_solved) > 20

    result = Result.model_validate_json(load_json(Path("./tests/res/out/testresult_s.json")))

    assert solved == result
