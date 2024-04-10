from pathlib import Path

import pytest

from app.solver.data.Job import Job, QNS, INS, NS
from app.solver.data.Result import Result, ResultEntry
from app.solver.solver import _solve_bruteforce, _solve_FFD, _solve_gapfill
from tests.conftest import load_json


def test_job_from_json():
    job = Job.model_validate_json(load_json(Path("./tests/res/in/testjob_multi.json")))
    assert job.__class__ == Job
    assert job.stocks[0].length == 1000


def test_result_from_json():
    result = Result.model_validate_json(load_json(Path("./tests/res/out/testresult_multi.json")))
    assert result.__class__ == Result
    assert result.layout[0].trimming == 0
    assert result.layout[2].stock.length == 1000


@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_job_to_result_json(solver):
    job = Job.model_validate_json(load_json(Path("./tests/res/in/testjob_multi.json")))
    result = Result.model_validate_json(load_json(Path("./tests/res/out/testresult_multi.json")))
    solved = solver(job)

    assert job == result.job
    assert solved == result.layout


@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_solver_single(solver):
    job = Job(stocks=(INS(length=1010),), cut_width=10, required=(QNS(length=500, quantity=4),))
    solved = solver(job)

    assert solved == (
        ResultEntry(stock=job.stocks[0].as_base(), cuts=(NS(length=500), NS(length=500)), trimming=0),
        ResultEntry(stock=job.stocks[0].as_base(), cuts=(NS(length=500), NS(length=500)), trimming=0),
    )


# @pytest.mark.skip(reason="bug #52")
@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_solver_multi(solver):
    job = Job(stocks=(INS(length=1100), INS(length=500, quantity=2)), cut_width=10,
              required=(QNS(length=500, quantity=4),))
    solved = solver(job)

    assert solved == (
        ResultEntry(stock=job.stocks[1].as_base(), cuts=(NS(length=500),), trimming=0),
        ResultEntry(stock=job.stocks[1].as_base(), cuts=(NS(length=500),), trimming=0),
        ResultEntry(stock=job.stocks[0].as_base(), cuts=(NS(length=500), NS(length=500)), trimming=80),
    )
