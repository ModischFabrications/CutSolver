import math
from math import factorial, prod
from typing import Iterator, Optional

from pydantic import BaseModel, ConfigDict, PositiveInt, NonNegativeInt, model_validator


class NamedSize(BaseModel):
    # frozen might be nice, but that would make reuse in solvers worse
    model_config = ConfigDict(validate_assignment=True)

    length: PositiveInt
    name: Optional[str] = None

    def __lt__(self, other):
        """
        compares lengths
        """
        return self.length < other.length

    def __hash__(self) -> int:
        return hash((self.length, self.name))

    def __str__(self):
        return f"{self.name}: l={self.length}"


class TargetStock(NamedSize):
    pass


class TargetSize(NamedSize):
    quantity: PositiveInt

    def __str__(self):
        return f"{self.name}: l={self.length}, n={self.quantity}"

    def as_base(self) -> NamedSize:
        return NamedSize(length=self.length, name=self.name)


class StockSize(TargetStock):
    quantity: PositiveInt = 999  # more or less equal to infinite

    def iterate_sizes(self) -> Iterator[TargetStock]:
        """
        yields all lengths times amount, sorted descending
        """

        for _ in range(self.quantity):
            yield TargetStock(length=self.length, name=self.name)

    def as_base(self) -> TargetStock:
        return TargetStock(length=self.length, name=self.name)


class Job(BaseModel):
    model_config = ConfigDict(frozen=True, validate_assignment=True)

    cut_width: NonNegativeInt = 0
    stocks: tuple[StockSize, ...]
    required: tuple[TargetSize, ...]

    def iterate_sizes(self) -> Iterator[NamedSize]:
        """
        yields all lengths times amount, sorted descending
        """

        # sort descending to favor combining larger sizes first
        for target in sorted(self.required, key=lambda x: x.length, reverse=True):
            for _ in range(target.quantity):
                yield target.as_base()

    def n_targets(self) -> int:
        """
        Number of possible combinations of target sizes
        """
        return sum([target.quantity for target in self.required])

    def n_combinations(self) -> float | int:
        """
        Number of possible combinations of target sizes; returns infinite if too large
        """
        if self.n_targets() > 100:
            return math.inf
        return int(factorial(self.n_targets()) / prod([factorial(n.quantity) for n in self.required]))

    @model_validator(mode='after')
    def assert_valid(self) -> 'Job':
        # basic assertion are done at field level
        if len(self.stocks) <= 0:
            raise ValueError(f"Job is missing stocks")
        if len(self.required) <= 0:
            raise ValueError("Job is missing required")

        if any(all(target.length > stock.length for stock in self.stocks) for target in self.required):
            raise ValueError("Job has target sizes longer than the stock")
        return self

    def __eq__(self, other):
        return (
                self.stocks == other.stocks
                and self.cut_width == other.cut_width
                and self.required == other.required
        )

    def __hash__(self) -> int:
        return hash((str(sorted(self.stocks)), self.cut_width, str(sorted(self.required))))
