from app.solver.solver import (
    _get_trimming,
    _get_trimmings,
    _solve_bruteforce,
    _solve_gapfill,
    _solve_FFD,
    distribute,
)
from tests.test_fixtures import *


def test_trimming():
    trimming = _get_trimming(
        max_length=1500,
        lengths=((500, ""), (500, ""), (400, "")),
        cut_width=10,
    )

    assert trimming == 70


def test_trimming_zero():
    trimming = _get_trimming(
        max_length=1500,
        lengths=((500, ""), (500, ""), (480, "")),
        cut_width=10,
    )

    assert trimming == 0


def test_trimming_raise():
    # raises Error if more stock was used than available
    with pytest.raises(OverflowError):
        _get_trimming(1500, ((300, ""), (400, ""), (600, ""), (200, "")), 2)


def test_trimmings():
    trimming = _get_trimmings(
        max_length=1500,
        lengths=(((500, ""), (500, ""), (400, "")), ((500, ""), (500, ""), (400, ""))),
        cut_width=10,
    )

    assert trimming == 140


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


def test_full_solver():
    json_job = Path("./tests/res/in/testjob_s.json")
    assert json_job.exists()

    json_result = Path("./tests/res/out/testresult_s.json")

    with open(json_job, "r") as encoded_job:
        job = Job.model_validate_json(encoded_job.read())

        solved = distribute(job)

        encoded_solved = solved.model_dump_json()
        assert len(encoded_solved) > 20

    with open(json_result, "r") as encoded_result:
        result = Result.model_validate_json(encoded_result.read())

        assert solved == result
