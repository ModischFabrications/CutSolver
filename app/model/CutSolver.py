#!python3
import copy
from itertools import permutations
from time import perf_counter
from typing import Collection, Tuple, List

from app.model.Job import Job
from app.model.Result import SolverType, Result

# backend parameter
n_max_precise = 10  # 10! calculations, around 3 million
n_max_good = 100
n_max = 500  # around 1 million with n^2


def distribute(job: Job) -> Result:
    # optimize before distibuting
    # job.compress()

    result: Result
    time: float = perf_counter()

    if len(job) <= n_max_precise:
        result = _solve_bruteforce(job)
    elif len(job) <= n_max_good:
        result = _solve_FFD(job)
    elif len(job) <= n_max:
        result = _solve_gapfill(job)
    else:
        raise OverflowError("Input too large")

    result.time_us = int((perf_counter() - time) * 1000 * 1000)
    return result


# CPU-bound
# O(n!)
def _solve_bruteforce(job: Job) -> Result:
    # failsafe
    if len(job) > 12:
        raise OverflowError("Input too large")

    # find every possible ordering (n! elements)
    all_orderings = permutations(job.get_sizes())
    # TODO: remove duplicates (due to "quantity")

    # "infinity"
    min_trimmings = len(job) * job.max_length
    min_stocks: List[List[int]] = []

    # possible improvement: Distribute combinations to multiprocessing worker threads
    for combination in all_orderings:
        stocks, trimmings = _split_combination(combination, job.max_length, job.cut_width)
        if trimmings < min_trimmings:
            min_stocks = stocks
            min_trimmings = trimmings

    return Result(solver_type=SolverType.bruteforce, lengths=min_stocks)


def _split_combination(combination: Tuple[int], max_length: int, cut_width: int):
    """
    Collects sizes until length is reached, then starts another stock
    :param combination:
    :param max_length:
    :param cut_width:
    :return:
    """
    stocks: List[List[int]] = []
    trimmings = 0

    current_size = 0
    current_stock: List[int] = []
    for size in combination:
        if (current_size + size + cut_width) > max_length:
            # start next stock
            stocks.append(current_stock)
            trimmings += _get_trimming(max_length, current_stock, cut_width)
            current_size = 0
            current_stock: List[int] = []

        current_size += (size + cut_width)
        current_stock.append(size)
    # catch leftovers
    if current_stock:
        stocks.append(current_stock)
        trimmings += _get_trimming(max_length, current_stock, cut_width)
    return stocks, trimmings


# TODO: check if time varies with len(TargetSize) or TargetSize.quantity
# this might actually be worse than FFD (both in runtime and solution)
# O(n^2) ??
def _solve_gapfill(job: Job) -> Result:
    # 1. Sort by magnitude (largest first)
    # 2. stack until limit is reached
    # 3. try smaller as long as possible
    # 4. create new bar

    # we are writing around in target sizes, prevent leaking changes to job
    mutable_sizes = copy.deepcopy(job.target_sizes)
    targets = sorted(mutable_sizes, reverse=True)

    stocks = []

    current_size = 0
    current_stock = []

    i_target = 0
    while len(targets) > 0:

        # nothing fit, next stock
        if i_target >= len(targets):
            # add local result
            stocks.append(current_stock)

            # reset
            current_stock = []
            current_size = 0
            i_target = 0

        current_target = targets[i_target]
        # target fits inside current stock, transfer to results
        if (current_size + current_target.length + job.cut_width) < job.max_length:
            current_stock.append(current_target.length)
            current_size += current_target.length + job.cut_width

            # remove empty entries
            if current_target.quantity <= 1:
                targets.remove(current_target)
            else:
                current_target.quantity -= 1
        # try smaller
        else:
            i_target += 1

    # apply last "forgotten" stock
    if current_stock:
        stocks.append(current_stock)

    # trimming could be calculated from len(stocks) * length - sum(stocks)
    return Result(solver_type=SolverType.gapfill, lengths=stocks)


# textbook solution, guaranteed to need at most double
# TODO this has ridiculous execution times, check why
def _solve_FFD(job: Job) -> Result:
    # iterate over list of stocks
    # put into first stock that it fits into

    # 1. Sort by magnitude (largest first)
    # 2. stack until limit is reached
    # 3. try smaller as long as possible
    # 4. create new bar

    mutable_sizes = copy.deepcopy(job.target_sizes)
    targets = sorted(mutable_sizes, reverse=True)

    assert len(targets) > 0

    stocks: List[List[int]] = [[]]
    stock_lengths: List[int] = [0]

    i_target = 0

    while i_target < len(targets):
        current_size = targets[i_target]

        for i, stock in enumerate(stocks):
            # step through existing stocks until current size fits
            if (job.max_length - stock_lengths[i]) > current_size.length:
                # add size
                stock.append(current_size.length)
                stock_lengths[i] += job.cut_width + current_size.length
                break
        else:  # nothing fit, opening next bin
            stocks.append([current_size.length])
            stock_lengths.append(0)

            assert len(stocks) == len(stock_lengths)

        # decrease/get next
        if current_size.quantity <= 1:
            i_target += 1
        else:
            current_size.quantity -= 1

    return Result(solver_type=SolverType.FFD, lengths=stocks)


def _get_trimming(max_length: int, lengths: Collection[int], cut_width: int) -> int:
    sum_lengths = sum(lengths)
    sum_cuts = len(lengths) * cut_width

    trimmings = max_length - (sum_lengths + sum_cuts)

    if trimmings < 0:
        raise OverflowError

    return trimmings
