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
