from enum import unique, Enum
from typing import List

from pydantic import BaseModel


@unique
class SolverType(str, Enum):  # str as base enables Pydantic-Schemas
    bruteforce = "bruteforce"
    gapfill = "gapfill"
    FFD = "FFD"


class Result(BaseModel):
    solver_type: SolverType
    time_us: int = -1
    lengths: List[List[int]]

    # no trimmings as they can be inferred from stocks

    def __eq__(self, other):
        return self.solver_type == other.solver_type and \
               self.lengths == other.lengths

    def exactly(self, other):
        return self.solver_type == other.solver_type and \
               self.time_us == other.time_us and \
               self.lengths == other.lengths

    def valid(self):
        return self.solver_type in SolverType and self.time_us >= 0 and len(self.lengths) > 0
