import shelve
from pathlib import Path

# TODO: find a directory that is always writable
# win: appdata/*
# linux:
file_path = Path("data/SolverStore.db")

# writeback is slower but easier
d = shelve.open(str(file_path), writeback=True)


def get_ID():
    return d.get("job_id", 0)


def set_ID(ID: int):
    d["job_id"] = ID


def reset_ID():
    d["job_id"] = 0
