import math
from math import factorial, prod
from typing import Iterator, Optional

from pydantic import BaseModel, ConfigDict, PositiveInt, NonNegativeInt, model_validator


class NS(BaseModel):
    """
    "named size", wraps length + name
    """
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


# TODO this should probably be inlined
class ResultStock(NS):
    pass


class TS(NS):
    """
    "target size", adds quantity
    """
    quantity: PositiveInt

    def __str__(self):
        return f"{self.name}: l={self.length}, n={self.quantity}"

    def as_base(self) -> NS:
        return NS(length=self.length, name=self.name)


class StockSize(ResultStock):
    """
    "stock size", adds optional quantity (can be infinite)
    """
    quantity: Optional[PositiveInt] = -1  # more or less equal to infinite

    def as_base(self) -> ResultStock:
        return ResultStock(length=self.length, name=self.name)

    def safe_quantity(self):
        return self.quantity if self.quantity > 0 else 999


class Job(BaseModel):
    model_config = ConfigDict(frozen=True, validate_assignment=True)

    cut_width: NonNegativeInt = 0
    stocks: tuple[StockSize, ...]
    required: tuple[TS, ...]

    def iterate_required(self) -> Iterator[NS]:
        """
        yields all lengths times amount, sorted descending
        """

        # sort descending to favor combining larger sizes first
        for target in sorted(self.required, reverse=True):
            for _ in range(target.quantity):
                yield target.as_base()

    def iterate_stocks(self) -> Iterator[ResultStock]:
        """
        yields all lengths times amount (including unwrapped infinite stocks);
        sorted descending
        """

        # sort descending to favor combining larger sizes first
        for target in sorted(self.stocks, reverse=True):
            # if this overflows your solution is probably shit; add +1 if unsure
            iterations = target.quantity if target.quantity != -1 else math.ceil(
                self.sum_of_required() / target.length)
            for _ in range(iterations):
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
        # TODO extend with multiplication by stock permutations
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

        # this isn't perfect and requires additional calculations for cuts
        if (
                self.sum_of_required() >
                sum([stock.length for stock in self.iterate_stocks()])
        ):
            raise ValueError("Job has more targets than the stock available")

        return self

    def sum_of_required(self):
        return sum([target.length * target.quantity for target in self.required])

    def __eq__(self, other):
        return (
                self.stocks == other.stocks
                and self.cut_width == other.cut_width
                and self.required == other.required
        )

    def __hash__(self) -> int:
        return hash((str(sorted(self.stocks)), self.cut_width, str(sorted(self.required))))
