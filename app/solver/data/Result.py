from enum import unique, Enum
from typing import Optional, TypeAlias

from pydantic import BaseModel, PositiveInt, model_validator, ConfigDict

from app.solver.data.Job import Job


@unique
class SolverType(str, Enum):  # str as base enables Pydantic-Schemas
    bruteforce = "bruteforce"
    gapfill = "gapfill"
    FFD = "FFD"


ResultLength: TypeAlias = tuple[tuple[PositiveInt, str | None], ...]
ResultLengths: TypeAlias = tuple[ResultLength, ...]


class Result(BaseModel):
    model_config = ConfigDict(frozen=True, validate_assignment=True)

    job: Job
    solver_type: SolverType
    time_us: Optional[PositiveInt] = None
    lengths: ResultLengths

    # no trimmings as they can be inferred from difference to job

    # these could sort but there is no need with pre-sorted solvers
    def __eq__(self, other):
        return (
                self.job == other.job
                and self.solver_type == other.solver_type
                and self.lengths == other.lengths
        )

    def exactly(self, other):
        return (
                self.job == other.job
                and self.solver_type == other.solver_type
                and self.time_us == other.time_us
                and self.lengths == other.lengths
        )

    @model_validator(mode='after')
    def assert_valid(self):
        if self.solver_type not in SolverType:
            raise ValueError(f"Result has invalid solver_type {self.solver_type}")
        if len(self.lengths) <= 0:
            raise ValueError("Result is missing lengths")
        return self
