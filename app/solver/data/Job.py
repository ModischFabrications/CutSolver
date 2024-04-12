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
        if self.name:
            return f"{self.name}: l={self.length}"
        return f"l={self.length}"

    def __repr__(self):
        if self.name:
            return f"NS(length={self.length}, name={self.name})"
        return f"NS(length={self.length})"


class QNS(NS):
    """
    "quantity + named size", adds quantity
    """
    quantity: PositiveInt

    def __str__(self):
        return f"{self.name}: l={self.length}, n={self.quantity}"

    def __repr__(self):
        if self.name:
            return f"QNS(length={self.length}, name={self.name}, quantity={self.quantity})"
        return f"QNS(length={self.length}, quantity={self.quantity})"

    def as_base(self) -> NS:
        return NS(length=self.length, name=self.name)


class INS(NS):
    """
    "(infinite) quantity + named size", adds optional quantity (can be infinite)
    """
    quantity: Optional[PositiveInt] = None  # more or less equal to infinite

    def as_base(self) -> NS:
        return NS(length=self.length, name=self.name)


class Job(BaseModel):
    model_config = ConfigDict(frozen=True, validate_assignment=True)

    cut_width: NonNegativeInt = 0
    stocks: tuple[INS, ...]
    required: tuple[QNS, ...]

    def iterate_required(self) -> Iterator[NS]:
        """
        yields all lengths times amount, sorted descending
        """

        # sort descending to favor combining larger sizes first
        for target in sorted(self.required, reverse=True):
            for _ in range(target.quantity):
                yield target.as_base()

    def iterate_stocks(self) -> Iterator[NS]:
        """
        yields all lengths times amount (including unwrapped infinite stocks);
        sorted descending
        skips irrelevant entries
        """

        # sort descending to favor combining larger sizes first
        for target in sorted(self.stocks, reverse=True):
            # removal could happen during validation, but we want frozen, immutable jobs
            if all(req.length > target.length for req in self.required):
                # print(f"Skipping {target}, too short for requirements")
                continue

            # if this overflows your solution is probably shit
            # x2 because the worst layout possible is a duplicate a tiny bit over
            # TODO this could be reduced further
            iterations = target.quantity if target.quantity else math.ceil(
                (self.sum_of_required() * 2) / target.length)
            for _ in range(iterations):
                yield target.as_base()

    def sum_of_required(self):
        # won't account for layouts! easy to trick
        return sum([(target.length + self.cut_width) * target.quantity for target in self.required])

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
            raise ValueError("Job has no stocks")
        if len(self.required) <= 0:
            raise ValueError("Job has no required")

        if any(all(target.length > stock.length for stock in self.stocks) for target in self.required):
            raise ValueError("Job has target sizes longer than the stock")

        # this isn't perfect and requires additional calculations for cuts
        if (
                self.sum_of_required() >
                sum([stock.length for stock in self.iterate_stocks()])
        ):
            raise ValueError("Job has more targets than the stock available")

        return self

    def __eq__(self, other):
        return (
                self.stocks == other.stocks
                and self.cut_width == other.cut_width
                and self.required == other.required
        )

    def __hash__(self) -> int:
        return hash((str(sorted(self.stocks)), self.cut_width, str(sorted(self.required))))
