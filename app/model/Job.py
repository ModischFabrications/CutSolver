from enum import Enum, unique
from typing import Iterator, List

from pydantic import BaseModel


class TargetSize(BaseModel):
    length: int
    amount: int

    def __lt__(self, other):
        """
        compares lengths
        """
        return self.length < other.length

    def __str__(self):
        return f"l:{self.length}, n:{self.amount}"


class Job(BaseModel):
    length_stock: int
    target_sizes: List[TargetSize]
    cut_width: int = 0

    # utility

    def get_sizes(self) -> Iterator[int]:
        """
        yields all lengths
        """
        for size in self.target_sizes:
            for i in range(size.amount):
                yield size.length

    def __len__(self) -> int:
        """
        Number of target sizes in job
        """
        return sum(target.amount for target in self.target_sizes)

    def __eq__(self, other):
        return self.length_stock == other.length_stock and self.target_sizes == other.target_sizes and self.cut_width == other.cut_width


@unique
class SolverType(str, Enum):  # str as base enables Pydantic-Schemas
    bruteforce = "bruteforce"
    gapfill = "gapfill"
    FFD = "FFD"


class Result(BaseModel):
    stocks: List[List[int]]
    # no trimmings as they can be inferred from stocks
    solver: SolverType
