#!python3

from typing import Collection, Tuple


class TargetSize:
    def __init__(self, length: int, amount: int):
        self.length = length
        self.amount = amount

    def __lt__(self, other):
        return self.length < other.length


class Job:
    current_id = 0

    def __init__(self, length_stock: int, target_sizes: Collection[TargetSize], cut_width: int = 5):
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
    n_max = 1000        # unreasonable time TODO might use timer instead

    @staticmethod
    def distribute(job: Job) -> Tuple[Collection[Collection[int]], int]:

        if len(job.target_sizes) < Solver.n_max_precise:
            return Solver._solve_bruteforce(job)
        elif len(job.target_sizes) < Solver.n_max:
            return Solver._solve_heuristic(job)
        else:
            raise OverflowError("Input too large")

    # CPU-bound
    @staticmethod
    def _solve_bruteforce(job: Job) -> Tuple[Collection[Collection[int]], int]:
        raise NotImplementedError()
        # TODO: find every possible ordering
        # calculate trimming for each bar

        # use multiprocessing to utilise multiple cores

    # TODO: check if time varies with len(TargetSize) or TargetSize.amount
    @staticmethod
    def _solve_heuristic(job: Job) -> Tuple[Collection[Collection[int]], int]:
        # input

        # TODO:
        # 1. Sort by magnitude (largest first)
        # 2. stack until limit is reached
        # 3. try smaller as long as possible
        # 4. create new bar

        targets = sorted(job.target_sizes, reverse=True)

        stocks = []
        trimming = 0

        current_size = 0
        current_stock = []

        i_target = 0
        while len(targets) > 0:

            # nothing fit, next stock
            if i_target >= len(targets):
                stocks.append(current_stock)

                trimming += Solver._get_trimming(job.length_stock, current_stock, job.cut_width)

                current_stock = []
                current_size = 0
                i_target = 0

            current_target = targets[i_target]
            # target fits inside current stock, transfer to results
            if (current_size + current_target.length + job.cut_width) < job.length_stock:
                current_stock.append(current_target.length)
                current_size += current_target.length

                if current_target.amount <= 0:
                    targets.remove(current_target)  # FIXME Index probably here
                else:
                    current_target.amount -= 1
            # try smaller
            else:
                i_target += 1

        # (500, 500, 400), (400, 400, 400)
        return stocks, trimming

    @staticmethod
    def _get_trimming(length_stock: int, lengths: Collection[int], cut_width: int) -> int:
        sum_lengths = sum(lengths)
        sum_cuts = len(lengths) * cut_width

        trimmings = length_stock - (sum_lengths + sum_cuts)

        if trimmings < 0:
            raise OverflowError

        return trimmings
