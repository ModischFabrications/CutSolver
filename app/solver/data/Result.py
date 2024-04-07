from enum import unique, Enum
from typing import Optional

from pydantic import BaseModel, PositiveInt, model_validator, ConfigDict, NonNegativeInt

from app.solver.data.Job import Job, NamedSize, TargetStock


@unique
class SolverType(str, Enum):  # str as base enables Pydantic-Schemas
    bruteforce = "bruteforce"
    gapfill = "gapfill"
    FFD = "FFD"


class ResultEntry(BaseModel):
    model_config = ConfigDict(frozen=True, validate_assignment=True)

    stock: TargetStock
    cuts: tuple[NamedSize, ...]
    trimming: NonNegativeInt

    def __lt__(self, other):
        # this could also sort by trimmings, not sure if that is better
        return len(self.cuts)


class Result(BaseModel):
    model_config = ConfigDict(frozen=True, validate_assignment=True)

    job: Job
    solver_type: SolverType
    time_us: Optional[PositiveInt] = None
    # keep most cuts at the top, getting simpler towards the end
    layout: tuple[ResultEntry, ...]

    def trimmings(self):
        """
        trimmings are summed from entries on demand
        """
        return sum([t.trimming for t in self.layout])

    # these could sort but there is no need with pre-sorted solvers
    def __eq__(self, other):
        return (
                self.job == other.job
                and self.solver_type == other.solver_type
                and self.layout == other.layout
        )

    def exactly(self, other):
        return (
                self.job == other.job
                and self.solver_type == other.solver_type
                and self.time_us == other.time_us
                and self.layout == other.layout
        )

    @model_validator(mode='after')
    def assert_valid(self):
        # basic assertion are done at field level
        if len(self.layout) <= 0:
            raise ValueError("Result is missing lengths")
        return self
