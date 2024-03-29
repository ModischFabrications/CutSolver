#!python3
import copy
from itertools import permutations
from time import perf_counter
from typing import Collection, Tuple, List

from app.constants import n_max_precise, n_max
from app.solver.data.Job import Job, TargetSize
from app.solver.data.Result import SolverType, Result


def distribute(job: Job) -> Result:
    time: float = perf_counter()

    lengths: List[List[Tuple[int, str]]]
    solver_type: SolverType

    if len(job) <= n_max_precise:
        lengths = _solve_bruteforce(job)
        solver_type = SolverType.bruteforce
    elif len(job) <= n_max:
        lengths = _solve_FFD(job)
        solver_type = SolverType.FFD
    else:
        raise OverflowError("Input too large")

    time_us = int((perf_counter() - time) * 1000 * 1000)

    return Result(job=job, solver_type=solver_type, time_us=time_us, lengths=lengths)


# CPU-bound
# O(n!)
def _solve_bruteforce(job: Job) -> List[List[Tuple[int, str | None]]]:
    # failsafe
    if len(job) > 12:
        raise OverflowError("Input too large")

    mutable_job = job.model_copy(deep=True)
    # allow "overflowing" cut at the end
    mutable_job.max_length += mutable_job.cut_width

    # find every possible ordering (n! elements)
    all_orderings = permutations(job.iterate_sizes())
    # TODO: remove duplicates (due to "quantity")
    all_orderings = permutations(mutable_job.iterate_sizes())

    # "infinity"
    minimal_trimmings = len(mutable_job) * mutable_job.max_length
    best_stock: List[List[Tuple[int, str | None]]] = []

    # possible improvement: Distribute combinations to multiprocessing worker threads
    for combination in all_orderings:
        stocks, trimmings = _split_combination(
            combination, mutable_job.max_length, mutable_job.cut_width
        )
        if trimmings < minimal_trimmings:
            best_stock = stocks
            minimal_trimmings = trimmings

    return _sorted(best_stock)


def _split_combination(
        combination: Tuple[Tuple[int, str | None]], max_length: int, cut_width: int
):
    """
    Collects sizes until length is reached, then starts another stock
    :param combination:
    :param max_length:
    :param cut_width:
    :return:
    """
    stocks: List[List[Tuple[int, str | None]]] = []
    trimmings = 0

    current_size = 0
    current_stock: List[Tuple[int, str | None]] = []
    for size, name in combination:
        if (current_size + size + cut_width) > max_length:
            # start next stock
            stocks.append(current_stock)
            trimmings += _get_trimming(max_length, current_stock, cut_width)
            current_size = 0
            current_stock: List[Tuple[int, str | None]] = []

        current_size += size + cut_width
        current_stock.append((size, name))
    # catch leftovers
    if current_stock:
        stocks.append(current_stock)
        trimmings += _get_trimming(max_length, current_stock, cut_width)
    return stocks, trimmings


# this might actually be worse than FFD (both in runtime and solution), disabled for now
# O(n^2) ??
def _solve_gapfill(job: Job) -> List[List[Tuple[int, str | None]]]:
    # 1. Sort by magnitude (largest first)
    # 2. stack until limit is reached
    # 3. try smaller as long as possible
    # 4. create new bar

    # TODO: rewrite to use native map instead
    # we are writing around in target sizes, prevent leaking changes to job
    mutable_sizes = copy.deepcopy(job.sizes_as_list())
    targets = sorted(mutable_sizes, reverse=True)

    stocks = []

    current_size = 0
    current_stock: List[Tuple[int, str | None]] = []

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

        current_target: TargetSize = targets[i_target]
        # target fits inside current stock, transfer to results
        if (current_size + current_target.length + job.cut_width) < job.max_length:
            current_stock.append((current_target.length, current_target.name))
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
    return _sorted(stocks)


# textbook solution, guaranteed to get at most double trimmings of perfect solution
def _solve_FFD(job: Job) -> List[List[Tuple[int, str | None]]]:
    # iterate over list of stocks
    # put into first stock that it fits into

    # 1. Sort by magnitude (largest first)
    # 2. stack until limit is reached
    # 3. try smaller as long as possible
    # 4. create new bar

    # TODO: rewrite to use native map instead?
    mutable_sizes = copy.deepcopy(job.sizes_as_list())
    sizes = sorted(mutable_sizes, reverse=True)

    stocks: List[List[Tuple[int, str | None]]] = [[]]

    i_target = 0

    while i_target < len(sizes):
        current_size = sizes[i_target]
        for stock in stocks:
            # calculate current stock length
            stock_length = (
                    sum([size[0] for size in stock]) + (len(stock) - 1) * job.cut_width
            )
            # step through existing stocks until current size fits
            if (job.max_length - stock_length) > current_size.length:
                # add size
                stock.append((current_size.length, current_size.name))
                break
        else:  # nothing fit, opening next bin
            stocks.append([(current_size.length, current_size.name)])

        # decrease/get next
        if current_size.quantity <= 1:
            i_target += 1
        else:
            current_size.quantity -= 1

    return _sorted(stocks)


def _get_trimming(
        max_length: int, lengths: Collection[Tuple[int, str | None]], cut_width: int
) -> int:
    sum_lengths = sum([length[0] for length in lengths])
    sum_cuts = len(lengths) * cut_width

    trimmings = max_length - (sum_lengths + sum_cuts)

    if trimmings < 0:
        raise OverflowError

    return trimmings


def _get_trimmings(
        max_length: int, lengths: Collection[Collection[Tuple[int, str | None]]], cut_width: int
) -> int:
    return sum(_get_trimming(max_length, x, cut_width) for x in lengths)

def _sorted(lengths: List[List[Tuple[int, str | None]]]) -> List[List[Tuple[int, str | None]]]:
    # keep most cuts at the top, getting simpler towards the end
    # this could also sort by trimmings but that is more work
    return sorted(lengths, key=len, reverse=True)
