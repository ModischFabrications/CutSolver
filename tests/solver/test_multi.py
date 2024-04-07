from pathlib import Path

import pytest

from app.solver.data.Job import Job, TargetSize, StockSize, NamedSize
from app.solver.data.Result import Result, ResultEntry
from app.solver.solver import _solve_bruteforce, _solve_FFD, _solve_gapfill
from tests.test_fixtures import load_json


def test_job_from_json():
    job = Job.model_validate_json(load_json(Path("./tests/res/in/testjob_multi.json")))
    assert job.__class__ == Job
    assert job.assert_valid
    assert job.stocks[0].length == 1000


def test_result_from_json():
    result = Result.model_validate_json(load_json(Path("./tests/res/out/testresult_multi.json")))
    assert result.__class__ == Result
    assert result.assert_valid
    assert result.layout[0].stock.length == 1000


# @pytest.mark.skip(reason="bug #52")
@pytest.mark.parametrize("solver", [_solve_bruteforce, _solve_FFD, _solve_gapfill])
def test_solver(solver):
    job = Job(stocks=(StockSize(length=1010),), cut_width=10, required=(TargetSize(length=500, quantity=4),))
    solved = solver(job)

    assert solved == (
        ResultEntry(stock=job.stocks[0], cuts=(NamedSize(length=500), NamedSize(length=500)), trimming=0),
        ResultEntry(stock=job.stocks[0], cuts=(NamedSize(length=500), NamedSize(length=500)), trimming=0),
    )
