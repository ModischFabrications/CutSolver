from enum import unique, Enum
from typing import List

from pydantic import BaseModel

from solver.data.Job import Job


@unique
class SolverType(str, Enum):  # str as base enables Pydantic-Schemas
    bruteforce = "bruteforce"
    gapfill = "gapfill"
    FFD = "FFD"


class Result(BaseModel):
    # allow IDs to skip redundant transmission for future versions
    job: Job
    solver_type: SolverType
    time_us: int = -1
    lengths: List[List[int]]

    # no trimmings as they can be inferred from difference to job

    def __eq__(self, other):
        return self.job == other.job and \
               self.solver_type == other.solver_type and \
               self.lengths == other.lengths

    def exactly(self, other):
        return self.job == other.job and \
               self.solver_type == other.solver_type and \
               self.time_us == other.time_us and \
               self.lengths == other.lengths

    def assert_valid(self):
        self.job.assert_valid()
        if self.solver_type not in SolverType:
            raise ValueError(f"Result has invalid solver_type {self.solver_type}")
        if self.time_us < 0:
            raise ValueError(f"Result has invalid time_us {self.time_us}")
        if len(self.lengths) <= 0:
            raise ValueError("Result is missing lengths")
