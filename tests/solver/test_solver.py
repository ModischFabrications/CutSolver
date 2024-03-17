from app.solver.solver import (
    _get_trimming,
    _solve_bruteforce,
    _solve_gapfill,
    _solve_FFD,
    distribute,
)
from tests.test_fixtures import *


def test_trimmings():
    trimming = _get_trimming(
        max_length=1500,
        lengths=((300, ""), (400, ""), (600, ""), (100, "")),
        cut_width=2,
    )

    assert trimming == 92


def test_trimmings_raise():
    # raises Error if more stock was used than available
    with pytest.raises(OverflowError):
        _get_trimming(1500, ((300, ""), (400, ""), (600, ""), (200, "")), 2)


def test_bruteforce(testjob_s):
    orig_job = testjob_s.model_copy(deep=True)
    solved = _solve_bruteforce(testjob_s)

    assert solved == [
        [(500, "Part1"), (500, "Part1"), (200, "Part2"), (200, "Part2")],
        [(200, "Part2"), (200, "Part2")],
    ]
    assert orig_job == testjob_s


def test_gapfill(testjob_s):
    orig_job = testjob_s.model_copy(deep=True)
    solved = _solve_gapfill(testjob_s)

    assert solved == [
        [(500, "Part1"), (500, "Part1"), (200, "Part2"), (200, "Part2")],
        [(200, "Part2"), (200, "Part2")],
    ]
    assert orig_job == testjob_s


def test_FFD(testjob_s):
    orig_job = testjob_s.model_copy(deep=True)
    solved = _solve_FFD(testjob_s)

    # assert solved == [[500, 500, 200, 200], [200, 200]]
    assert solved == [
        [(500, "Part1"), (500, "Part1"), (200, "Part2"), (200, "Part2")],
        [(200, "Part2"), (200, "Part2")],
    ]
    assert orig_job == testjob_s


def test_full_model():
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
