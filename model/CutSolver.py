#!python3

from typing import Collection


class TargetSize:
    def __init__(self, length: int, amount: int):
        self._length = length
        self._amount = amount


class Job:
    current_id = 0

    def __init__(self, length_stock: int, target_sizes: Collection[TargetSize], cut_width: int = 2):
        self._id = Job.current_id
        Job.current_id += 1

        self.length_stock = length_stock
        self.target_sizes = target_sizes
        self.cut_width = cut_width

    # utility

    def get_ID(self):
        return self._id

    def __eq__(self, other):
        return self._id == other.get_ID()


class Solver:
    # backend parameter
    n_max_precise = 20  # max 5sec per calculation

    def distribute(self, job: Job):
        if len(job.target_sizes) > Solver.n_max_precise:
            return self._solve_heuristic(job)
        else:
            return self._solve_bruteforce(job)

    # CPU-bound
    def _solve_bruteforce(self, job: Job):
        raise NotImplementedError()
        # TODO: find every possible ordering
        # calculate trimming for each bar

        # use multiprocessing to utilise multiple cores

    def _solve_heuristic(self, job: Job):
        raise NotImplementedError()

        # TODO:
        # 1. Sort by magnitude
        # 2. stack until limit was reached
        # 3. try smaller as long as possible,
        # 4. create new bar

    @staticmethod
    def _get_trimming(length_stock: int, lengths: Collection[int], cut_width: int):
        sum_lengths = sum(lengths)
        sum_cuts = len(lengths) * cut_width

        trimmings = length_stock - (sum_lengths + sum_cuts)

        if trimmings < 0:
            raise OverflowError

        return trimmings
