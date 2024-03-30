from math import factorial, prod
from typing import Iterator, Optional

from pydantic import BaseModel, ConfigDict, PositiveInt, NonNegativeInt, model_validator


class TargetSize(BaseModel):
    # frozen might be nice, but that would make reuse in solvers worse
    model_config = ConfigDict(validate_assignment=True)

    length: PositiveInt
    quantity: PositiveInt
    name: Optional[str] = ""

    def __lt__(self, other):
        """
        compares lengths
        """
        return self.length < other.length

    def __str__(self):
        return f"l:{self.length}, n:{self.quantity}"


class Job(BaseModel):
    model_config = ConfigDict(frozen=True, validate_assignment=True)

    max_length: PositiveInt
    cut_width: NonNegativeInt = 0
    target_sizes: tuple[TargetSize, ...]

    def iterate_sizes(self) -> Iterator[tuple[int, str | None]]:
        """
        yields all lengths, sorted descending
        """

        # sort descending to favor combining larger sizes first
        for target in sorted(self.target_sizes, key=lambda x: x.length, reverse=True):
            for _ in range(target.quantity):
                yield target.length, target.name

    def n_targets(self) -> int:
        """
        Number of possible combinations of target sizes
        """
        return sum([target.quantity for target in self.target_sizes])

    def n_combinations(self) -> int:
        """
        Number of possible combinations of target sizes
        """
        return int(factorial(self.n_targets()) / prod([factorial(n.quantity) for n in self.target_sizes]))

    @model_validator(mode='after')
    def assert_valid(self) -> 'Job':
        if self.max_length <= 0:
            raise ValueError(f"Job has invalid max_length {self.max_length}")
        if self.cut_width < 0:
            raise ValueError(f"Job has invalid cut_width {self.cut_width}")
        if len(self.target_sizes) <= 0:
            raise ValueError("Job is missing target_sizes")
        if any(target.length > self.max_length for target in self.target_sizes):
            raise ValueError("Job has target sizes longer than the stock")
        return self

    def __eq__(self, other):
        return (
                self.max_length == other.max_length
                and self.cut_width == other.cut_width
                and self.target_sizes == other.target_sizes
        )

    def __hash__(self) -> int:
        return hash((self.max_length, self.cut_width, str(sorted(self.target_sizes))))
