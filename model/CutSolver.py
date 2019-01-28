#!python3

from itertools import permutations
from typing import Collection, Tuple, List

from model.Job import Job


class Solver:
    # backend parameter
    n_max_precise = 10  # max 5sec per calculation
    n_max = 1000        # unreasonable time TODO might use timer instead

    @staticmethod
    def distribute(job: Job) -> Tuple[Collection[Collection[int]], int]:

        if len(job.target_sizes) < Solver.n_max_precise:
            return Solver._solve_bruteforce(job)
        elif len(job.target_sizes) < Solver.n_max:
            return Solver._solve_gapfill(job)
        else:
            raise OverflowError("Input too large")

    # CPU-bound
    # O(n!)
    @staticmethod
    def _solve_bruteforce(job: Job) -> Tuple[Collection[Collection[int]], int]:

        # failsafe
        if len(job) > 12:
            raise OverflowError("Input too large")

        # find every possible ordering (n! elements)
        all_orderings = permutations(job.get_sizes())
        # TODO: remove duplicates

        # "infinity"
        min_trimmings = len(job) * job.length_stock
        min_stocks: List[List[int]] = []

        # TODO: Distribute combinations to multiprocessing worker threads
        for combination in all_orderings:
            stocks, trimmings = Solver._split_combination(combination, job.length_stock, job.cut_width)
            if trimmings < min_trimmings:
                min_stocks = stocks
                min_trimmings = trimmings

        return min_stocks, min_trimmings

    @staticmethod
    def _split_combination(combination: Tuple[int], length_stock: int, cut_width: int):
        """
        Collects sizes until length is reached, then starts another stock
        :param combination:
        :param length_stock:
        :param cut_width:
        :return:
        """
        stocks: List[List[int]] = []
        trimmings = 0

        current_size = 0
        current_stock: List[int] = []
        for size in combination:
            if (current_size + size + cut_width) > length_stock:
                # start next stock
                stocks.append(current_stock)
                trimmings += Solver._get_trimming(length_stock, current_stock, cut_width)
                current_size = 0
                current_stock: List[int] = []

            current_size += (size + cut_width)
            current_stock.append(size)
        # catch leftovers
        if current_stock:
            stocks.append(current_stock)
            trimmings += Solver._get_trimming(length_stock, current_stock, cut_width)
        return stocks, trimmings

    # TODO: check if time varies with len(TargetSize) or TargetSize.amount
    # O(n^2)
    @staticmethod
    def _solve_gapfill(job: Job) -> Tuple[Collection[Collection[int]], int]:
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
                # add local result
                stocks.append(current_stock)
                trimming += Solver._get_trimming(job.length_stock, current_stock, job.cut_width)

                # reset
                current_stock = []
                current_size = 0
                i_target = 0

            current_target = targets[i_target]
            # target fits inside current stock, transfer to results
            if (current_size + current_target.length + job.cut_width) < job.length_stock:
                current_stock.append(current_target.length)
                current_size += current_target.length + job.cut_width

                # remove empty entries
                if current_target.amount <= 1:
                    targets.remove(current_target)
                else:
                    current_target.amount -= 1
            # try smaller
            else:
                i_target += 1

        # apply last "forgotten" stock
        if current_stock:
            stocks.append(current_stock)
            trimming += Solver._get_trimming(job.length_stock, current_stock, job.cut_width)

        # trimming could be calculated from len(stocks) * length - sum(stocks)
        return stocks, trimming

    # O(n)
    @staticmethod
    def _solve_FFD(job: Job) -> Tuple[Collection[Collection[int]], int]:
        # iterate over list of stocks
        # put into first stock that it fits into
        pass


    @staticmethod
    def _get_trimming(length_stock: int, lengths: Collection[int], cut_width: int) -> int:
        sum_lengths = sum(lengths)
        sum_cuts = len(lengths) * cut_width

        trimmings = length_stock - (sum_lengths + sum_cuts)

        if trimmings < 0:
            raise OverflowError

        return trimmings
