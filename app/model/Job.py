from typing import Collection, Iterator

from marshmallow import Schema, fields, post_load


class TargetSize:
    def __init__(self, length: int, amount: int):
        self.length = length
        self.amount = amount

    def __lt__(self, other):
        """
        compares lengths
        """
        return self.length < other.length

    def __str__(self):
        return f"l:{self.length}, n:{self.amount}"


class TargetSizeSchema(Schema):
    length = fields.Integer()
    amount = fields.Integer()

    @post_load
    def make_target_size(self, data):
        return TargetSize(**data)


class Job:
    _current_id = 0

    def __init__(self, length_stock: int, target_sizes: Collection[TargetSize], cut_width: int = 0):
        self._id = Job._current_id
        Job._current_id += 1

        self.length_stock = length_stock
        self.target_sizes = target_sizes
        self.cut_width = cut_width

    # utility

    def get_ID(self) -> int:
        return self._id

    def get_sizes(self) -> Iterator[int]:
        """
        yields all lengths
        """
        for size in self.target_sizes:
            for i in range(size.amount):
                yield size.length

    def __eq__(self, other):
        """
        Equality by ID, not by values
        """
        return self._id == other.get_ID()

    def __len__(self) -> int:
        """
        Number of target sizes in job
        """
        return sum(target.amount for target in self.target_sizes)


class JobSchema(Schema):
    length_stock = fields.Integer()
    target_sizes = fields.Nested(TargetSizeSchema, many=True)
    cut_width = fields.Integer()

    @post_load
    def make_job(self, data):
        return Job(**data)


class Result:
    def __init__(self, stocks: Collection[Collection[int]], trimmings: int):
        self.stocks = stocks
        self.trimmings = trimmings


class ResultSchema(Schema):
    stocks = fields.List(fields.List(fields.Integer()))
    trimmings = fields.Integer()

    @post_load
    def make_target_size(self, data):
        return Result(**data)
