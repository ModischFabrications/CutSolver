import pytest

from app.solver.data.Job import NS
from app.solver.data.Result import Result, SolverType, ResultEntry


def test_constructor(testjob_s):
    job = testjob_s
    result = Result(
        job=job,
        solver_type=SolverType.FFD,
        time_us=100,
        layout=(ResultEntry(stock=job.stocks[0],
                            cuts=(
                                NS(length=100, name="Part1"),
                                NS(length=100, name="Part1"),
                                NS(length=100, name="Part1"),
                            ),
                            trimming=1000
                            ),
                ResultEntry(stock=job.stocks[0],
                            cuts=(
                                NS(length=200, name="Part2"),
                                NS(length=200, name="Part2"),
                                NS(length=200, name="Part2"),
                            ),
                            trimming=700
                            )
                ))

    assert result

    def test_invalid(testjob_s):
        job = testjob_s

        with pytest.raises(ValueError):
            _ = Result(
                job=job,
                solver_type=SolverType.FFD,
                time_us=0,
                layout=(ResultEntry(stock=job.stocks[0],
                                    cuts=(
                                        NS(length=100, name="Part1"),
                                        NS(length=100, name="Part1"),
                                        NS(length=100, name="Part1"),
                                    ),
                                    trimming=1000
                                    ),))

            with pytest.raises(ValueError):
                _ = Result(
                    job=job,
                    time_us=999,
                    layout=(ResultEntry(stock=job.stocks[0],
                                        cuts=(
                                            NS(length=100, name="Part1"),
                                            NS(length=100, name="Part1"),
                                            NS(length=100, name="Part1"),
                                        ),
                                        trimming=1000
                                        ),))

    def test_equal(testjob_s):
        job = testjob_s
        result1 = Result(
            job=job,
            solver_type=SolverType.FFD,
            time_us=555,
            layout=(ResultEntry(stock=job.stocks[0],
                                cuts=(
                                    NS(length=100, name="Part1"),
                                    NS(length=100, name="Part1"),
                                    NS(length=100, name="Part1"),
                                ),
                                trimming=1000
                                ),))
        result2 = Result(
            job=job,
            solver_type=SolverType.FFD,
            time_us=999,
            layout=(ResultEntry(stock=job.stocks[0],
                                cuts=(
                                    NS(length=100, name="Part1"),
                                    NS(length=100, name="Part1"),
                                    NS(length=100, name="Part1"),
                                ),
                                trimming=1000
                                ),))

        assert result1 == result2

    def test_exactly(testjob_s):
        job = testjob_s
        result1 = Result(
            job=job,
            solver_type=SolverType.FFD,
            time_us=555,
            layout=(ResultEntry(stock=job.stocks[0],
                                cuts=(
                                    NS(length=100, name="Part1"),
                                    NS(length=100, name="Part1"),
                                    NS(length=100, name="Part1"),
                                ),
                                trimming=1000
                                ),))
        result2 = Result(
            job=job,
            solver_type=SolverType.FFD,
            time_us=999,
            layout=(ResultEntry(stock=job.stocks[0],
                                cuts=(
                                    NS(length=100, name="Part1"),
                                    NS(length=100, name="Part1"),
                                    NS(length=100, name="Part1"),
                                ),
                                trimming=1000
                                ),))
        result3 = Result(
            job=job,
            solver_type=SolverType.FFD,
            time_us=999,
            layout=(ResultEntry(stock=job.stocks[0],
                                cuts=(
                                    NS(length=100, name="Part1"),
                                    NS(length=100, name="Part1"),
                                    NS(length=100, name="Part1"),
                                ),
                                trimming=1000
                                ),))

        assert not result1.exactly(result2)
        assert result2.exactly(result3)
