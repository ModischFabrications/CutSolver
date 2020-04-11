from app.model.Result import Result, SolverType


def test_constructor():
    result = Result(solver_type=SolverType.FFD, time_us=100, lengths=[(100, 100, 100), (200, 200, 200)])
    assert result


def test_valid():
    result = Result(solver_type=SolverType.FFD, time_us=100, lengths=[(100, 100, 100), (200, 200, 200)])
    assert result.valid()


def test_invalid():
    invalid_result = Result(solver_type=SolverType.FFD, time_us=-1, lengths=[(100, 100, 100), (200, 200, 200)])
    assert not invalid_result.valid()


def test_equal():
    result1 = Result(solver_type=SolverType.FFD, time_us=100, lengths=[(100, 100, 100), (200, 200, 200)])
    result2 = Result(solver_type=SolverType.FFD, time_us=200, lengths=[(100, 100, 100), (200, 200, 200)])
    assert result1 == result2


def test_exactly():
    result1 = Result(solver_type=SolverType.FFD, time_us=100, lengths=[(100, 100, 100), (200, 200, 200)])
    result2 = Result(solver_type=SolverType.FFD, time_us=200, lengths=[(100, 100, 100), (200, 200, 200)])
    result3 = Result(solver_type=SolverType.FFD, time_us=200, lengths=[(100, 100, 100), (200, 200, 200)])
    assert not result1.exactly(result2)
    assert result2.exactly(result3)
