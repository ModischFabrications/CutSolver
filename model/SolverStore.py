import sqlite3
from pathlib import Path
# this will store Jobs and Results, identifiable by Job-ID
from sqlite3 import Cursor

from model import Job
from model.Job import Result

# TODO: find a directory that is always writable
# win: appdata/*
# linux:
file_path = Path("data/SolverStore.db").absolute()
_DB = sqlite3.connect(file_path)
_DB.execute("CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, job BLOB)")


class JobStorage:
    c: Cursor = _DB.cursor()

    @staticmethod
    def get_last_Job_ID() -> int:
        # nothing inserted yet
        if JobStorage.c.rowcount <= 0: return 0

        JobStorage.c.execute("SELECT max(id) FROM jobs")
        max_id = JobStorage.c.fetchone()[0]
        assert max_id >= 0
        return max_id

    def get_job(self, ID: int, delete=False) -> Job:
        raise NotImplementedError

    def add_job(self, job: Job):
        raise NotImplementedError
        _DB.commit()

    def cleanup(self):
        pass
        # ToDo: remove


class ResultStorage:
    c = _DB.cursor()

    def get_result(self, ID: int, delete=False) -> Result:
        raise NotImplementedError
        pass

    def add_result(self, result: Result):
        raise NotImplementedError
        _DB.commit()
