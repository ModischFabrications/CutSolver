import pytest

from solver.data.Result import Result, SolverType
from tests.test_utils import generate_testjob


def test_constructor():
    job = generate_testjob()
    result = Result(job=job, solver_type=SolverType.FFD, time_us=100, lengths=[(100, 100, 100), (200, 200, 200)])
    assert result


def test_valid():
    job = generate_testjob()
    result = Result(job=job, solver_type=SolverType.FFD, time_us=100, lengths=[(100, 100, 100), (200, 200, 200)])
    result.assert_valid()


def test_invalid():
    job = generate_testjob()
    invalid_result = Result(job=job, solver_type=SolverType.FFD, time_us=-1, lengths=[(100, 100, 100), (200, 200, 200)])
    with pytest.raises(ValueError):
        invalid_result.assert_valid()


def test_equal():
    job = generate_testjob()
    result1 = Result(job=job, solver_type=SolverType.FFD, time_us=100, lengths=[(100, 100, 100), (200, 200, 200)])
    result2 = Result(job=job, solver_type=SolverType.FFD, time_us=200, lengths=[(100, 100, 100), (200, 200, 200)])
    assert result1 == result2


def test_exactly():
    job = generate_testjob()
    result1 = Result(job=job, solver_type=SolverType.FFD, time_us=100, lengths=[(100, 100, 100), (200, 200, 200)])
    result2 = Result(job=job, solver_type=SolverType.FFD, time_us=200, lengths=[(100, 100, 100), (200, 200, 200)])
    result3 = Result(job=job, solver_type=SolverType.FFD, time_us=200, lengths=[(100, 100, 100), (200, 200, 200)])
    assert not result1.exactly(result2)
    assert result2.exactly(result3)
