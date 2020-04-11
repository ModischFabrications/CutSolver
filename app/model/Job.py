from typing import Iterator, List

from pydantic import BaseModel


class TargetSize(BaseModel):
    length: int
    quantity: int

    def __lt__(self, other):
        """
        compares lengths
        """
        return self.length < other.length

    def __str__(self):
        return f"l:{self.length}, n:{self.quantity}"


class Job(BaseModel):
    max_length: int
    target_sizes: List[TargetSize]
    cut_width: int = 0

    # utility

    def get_sizes(self) -> Iterator[int]:
        """
        yields all lengths
        """
        for size in self.target_sizes:
            for i in range(size.quantity):
                yield size.length

    def compress(self):
        """
        join TargetSizes that have the same length
        """
        known_sizes = dict()

        # list to dict to make them unique
        for size in self.target_sizes:
            if size.length in known_sizes:
                known_sizes[size.length] += size.quantity
            else:
                known_sizes[size.length] = size.quantity

        # back to list again for compatibility
        self.target_sizes = [TargetSize(length=l, quantity=q) for (l, q) in known_sizes.items()]

    def valid(self):
        return self.max_length > 0 and self.cut_width >= 0 and len(self.target_sizes) > 0

    def __len__(self) -> int:
        """
        Number of target sizes in job
        """
        return sum(target.quantity for target in self.target_sizes)

    def __eq__(self, other):
        return self.max_length == other.max_length and \
               self.target_sizes == other.target_sizes and \
               self.cut_width == other.cut_width
