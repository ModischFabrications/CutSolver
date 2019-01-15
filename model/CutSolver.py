#!python3

from typing import List, Dict, Tuple
from logging import Logger


class Job:
    def __init__(self, length_stock: int, cut_width: int = 2):
        self.length_stock = length_stock
        self.cut_width = cut_width



class Target:
    current_id = 0

    def __init__(self, length: int, amount: int):
        self._id = Target.current_id
        Target.current_id += 1

        self._length = length
        self._amount = amount

    @staticmethod
    def get_ID():
        return Target.current_id


class Solver:
    # backend parameter
    n_max_precise = 20  # max 5sec per calculation

    def distribute(self, length_stock: int, target_lengths: List[Target]):
        if len(target_lengths) > Solver.n_max_precise:
            return self._solve_heuristic(length_stock, target_lengths)
        else:
            return self._solve_bruteforce(length_stock, target_lengths)


    # CPU-bound
    def _solve_bruteforce(self, length_stock: int, target_lengths: List[Target]):
        raise NotImplementedError()
        # TODO: find every possible ordering
        # calculate trimming for each bar

        # use multiprocessing to utilise multiple cores

    def _solve_heuristic(self, length_stock: int, target_lengths: List[Target]):
        raise NotImplementedError()

        # TODO:
        # 1. Sort by magnitude
        # 2. stack until limit was reached
        # 3. try smaller as long as possible,
        # 4. create new bar

    def _get_trimming(self, length_stock: int, lengths: Tuple[int]):
        sum_lengths = sum(lengths)

        sum_cuts = sum_lengths

        if (sum_lengths > length_stock):

        return
