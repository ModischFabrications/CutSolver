import pytest

from app.solver.data.Result import Result, SolverType
from tests.test_fixtures import testjob_s


def test_constructor(testjob_s):
    job = testjob_s
    result = Result(
        job=job,
        solver_type=SolverType.FFD,
        time_us=100,
        lengths=[
            [
                (100, "Part1"),
                (100, "Part1"),
                (100, "Part1"),
            ],
            [
                (200, "Part2"),
                (200, "Part2"),
                (200, "Part2"),
            ],
        ],
    )
    assert result


def test_valid(testjob_s):
    job = testjob_s
    result = Result(
        job=job,
        solver_type=SolverType.FFD,
        time_us=100,
        lengths=[
            [
                (100, "Part1"),
                (100, "Part1"),
                (100, "Part1"),
            ],
            [
                (200, "Part2"),
                (200, "Part2"),
                (200, "Part2"),
            ],
        ],
    )


def test_invalid(testjob_s):
    job = testjob_s

    with pytest.raises(ValueError):
        no_job = Result(
            solver_type=SolverType.FFD,
            time_us=-1,
            lengths=[
                [
                    (100, "Part1"),
                    (100, "Part1"),
                    (100, "Part1"),
                ],
                [
                    (200, "Part2"),
                    (200, "Part2"),
                    (200, "Part2"),
                ],
            ],
        )

    with pytest.raises(ValueError):
        no_solve = Result(
            job=job,
            time_us=-1,
            lengths=[
                [
                    (100, "Part1"),
                    (100, "Part1"),
                    (100, "Part1"),
                ],
                [
                    (200, "Part2"),
                    (200, "Part2"),
                    (200, "Part2"),
                ],
            ],
        )


def test_equal(testjob_s):
    job = testjob_s
    result1 = Result(
        job=job,
        solver_type=SolverType.FFD,
        time_us=100,
        lengths=[
            [
                (100, "Part1"),
                (100, "Part1"),
                (100, "Part1"),
            ],
            [
                (200, "Part2"),
                (200, "Part2"),
                (200, "Part2"),
            ],
        ],
    )
    result2 = Result(
        job=job,
        solver_type=SolverType.FFD,
        time_us=200,
        lengths=[
            [
                (100, "Part1"),
                (100, "Part1"),
                (100, "Part1"),
            ],
            [
                (200, "Part2"),
                (200, "Part2"),
                (200, "Part2"),
            ],
        ],
    )
    assert result1 == result2


def test_exactly(testjob_s):
    job = testjob_s
    result1 = Result(
        job=job,
        solver_type=SolverType.FFD,
        time_us=100,
        lengths=[
            [
                (100, "Part1"),
                (100, "Part1"),
                (100, "Part1"),
            ],
            [
                (200, "Part2"),
                (200, "Part2"),
                (200, "Part2"),
            ],
        ],
    )
    result2 = Result(
        job=job,
        solver_type=SolverType.FFD,
        time_us=200,
        lengths=[
            [
                (100, "Part1"),
                (100, "Part1"),
                (100, "Part1"),
            ],
            [
                (200, "Part2"),
                (200, "Part2"),
                (200, "Part2"),
            ],
        ],
    )
    result3 = Result(
        job=job,
        solver_type=SolverType.FFD,
        time_us=200,
        lengths=[
            [
                (100, "Part1"),
                (100, "Part1"),
                (100, "Part1"),
            ],
            [
                (200, "Part2"),
                (200, "Part2"),
                (200, "Part2"),
            ],
        ],
    )
    assert not result1.exactly(result2)
    assert result2.exactly(result3)


def test_trimmings():
    trimming = Result(
        max_length=1500,
        lengths=(((500, ""), (500, ""), (400, "")), ((500, ""), (500, ""), (400, ""))),
        cut_width=10,
    )

    assert trimming == 140
