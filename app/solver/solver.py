#!python3
import copy
from itertools import permutations
from time import perf_counter
from typing import Collection

from app.constants import solverSettings
from app.solver.data.Job import Job, TargetSize
from app.solver.data.Result import SolverType, Result, ResultLengths


def distribute(job: Job) -> Result:
    time: float = perf_counter()

    lengths: ResultLengths
    solver_type: SolverType

    if job.n_combinations() <= solverSettings.bruteforce_max_combinations:
        lengths = _solve_bruteforce(job)
        solver_type = SolverType.bruteforce
    elif job.n_targets() <= solverSettings.n_max:
        lengths = _solve_FFD(job)
        solver_type = SolverType.FFD
    else:
        raise OverflowError("Input too large")

    time_us = int((perf_counter() - time) * 1000 * 1000)

    return Result(job=job, solver_type=solver_type, time_us=time_us, lengths=lengths)


# slowest, but perfect solver; originally O(n!), now much faster (see Job.n_combinations())
def _solve_bruteforce(job: Job) -> ResultLengths:
    mutable_job = job.model_copy(deep=True)
    mutable_job.model_config["frozen"] = False

    # allow "overflowing" cut at the end
    mutable_job.max_length += mutable_job.cut_width

    # find every possible ordering (`factorial(sum(sizes))` elements) and reduce to unique
    all_orderings = set(permutations(mutable_job.iterate_sizes()))

    # start at "all of it"
    minimal_trimmings = mutable_job.n_targets() * mutable_job.max_length
    best_results: list[list[list[tuple[int, str | None]]]] = []

    # could distribute to multiprocessing, but web worker is parallel anyway
    for combination in all_orderings:
        lengths, trimmings = _group_into_lengths(
            combination, mutable_job.max_length, mutable_job.cut_width
        )
        if trimmings < minimal_trimmings:
            best_stock = lengths
            minimal_trimmings = trimmings
            best_results.clear()
            best_results.append(best_stock)
        elif trimmings == minimal_trimmings:
            best_results.append(lengths)

    # set creates random order of perfect results due to missing sorting, so sort for determinism
    ordered = (sorted(
        set([tuple(sorted(
            [tuple(sorted(y, reverse=True)) for y in x], reverse=True)
        ) for x in best_results]), reverse=True
    ))
    # TODO evaluate which result aligns with user expectations best
    return _sorted(ordered[0])


def _group_into_lengths(
        combination: tuple[tuple[int, str | None], ...], max_length: int, cut_width: int
):
    """
    Collects sizes until length is reached, then starts another stock
    :param combination:
    :param max_length:
    :param cut_width:
    :return:
    """
    stocks: list[list[tuple[int, str | None]]] = []
    trimmings = 0

    current_size = 0
    current_stock: list[tuple[int, str | None]] = []
    for size, name in combination:
        if (current_size + size + cut_width) > max_length:
            # start next stock
            stocks.append(current_stock)
            trimmings += _get_trimming(max_length, current_stock, cut_width)
            current_size = 0
            current_stock = []

        current_size += size + cut_width
        current_stock.append((size, name))
    # catch leftovers
    if current_stock:
        stocks.append(current_stock)
        trimmings += _get_trimming(max_length, current_stock, cut_width)
    return stocks, trimmings


# textbook solution, guaranteed to get at most double trimmings of perfect solution; possibly O(n^2)?
def _solve_FFD(job: Job) -> ResultLengths:
    # iterate over list of stocks
    # put into first stock that it fits into

    # 1. Sort by magnitude (largest first)
    # 2. stack until limit is reached
    # 3. try smaller as long as possible
    # 4. create new bar

    mutable_sizes = copy.deepcopy(job.target_sizes)
    sizes = sorted(mutable_sizes, reverse=True)

    stocks: list[list[tuple[int, str | None]]] = [[]]

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


# even faster than FFD, seems like equal results; selfmade and less proven!
def _solve_gapfill(job: Job) -> ResultLengths:
    # 1. Sort by magnitude (largest first)
    # 2. stack until limit is reached
    # 3. try smaller as long as possible
    # 4. create new bar

    # we are writing around in target sizes, prevent leaking changes to job
    mutable_sizes = copy.deepcopy(job.target_sizes)
    targets = sorted(mutable_sizes, reverse=True)

    stocks = []

    current_size = 0
    current_stock: list[tuple[int, str | None]] = []

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
        if (current_size + current_target.length) <= job.max_length:
            current_stock.append((current_target.length, current_target.name))
            current_size += current_target.length
            if current_size < job.max_length:
                current_size += job.cut_width

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


def _get_trimming(
        max_length: int, lengths: Collection[tuple[int, str | None]], cut_width: int
) -> int:
    sum_lengths = sum([length[0] for length in lengths])
    sum_cuts = len(lengths) * cut_width

    trimmings = max_length - (sum_lengths + sum_cuts)

    # cut at the end can be omitted
    if trimmings == -cut_width:
        trimmings = 0

    if trimmings < 0:
        raise OverflowError("Trimmings can't ever be negative!")

    return trimmings


def _get_trimmings(max_length: int, lengths: ResultLengths, cut_width: int) -> int:
    return sum(_get_trimming(max_length, x, cut_width) for x in lengths)


def _sorted(lengths: Collection[Collection]) -> ResultLengths:
    # keep most cuts at the top, getting simpler towards the end
    # this could also sort by trimmings but that is more work
    lengths = tuple([tuple(sorted(l, reverse=True)) for l in lengths])
    return tuple(sorted(lengths, key=len, reverse=True))
