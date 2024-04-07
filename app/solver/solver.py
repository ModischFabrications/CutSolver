#!python3
import copy
from itertools import permutations
from time import perf_counter

from app.settings import solverSettings
from app.solver.data.Job import Job, TargetSize, NamedSize
from app.solver.data.Result import Result, SolverType, ResultEntry
from app.solver.utils import _get_trimming, create_result_entry, sort_entries, find_best_solution


def solve(job: Job) -> Result:
    time: float = perf_counter()

    layout: tuple[ResultEntry, ...]
    solver_type: SolverType

    if job.n_combinations() <= solverSettings.bruteforce_max_combinations:
        layout = _solve_bruteforce(job)
        solver_type = SolverType.bruteforce
    elif job.n_targets() <= solverSettings.solver_n_max:
        layout = _solve_FFD(job)
        solver_type = SolverType.FFD
    else:
        raise OverflowError("Input too large")

    time_us = int((perf_counter() - time) * 1000 * 1000)

    return Result(job=job, solver_type=solver_type, time_us=time_us, layout=layout)


# slowest, but perfect solver; originally O(n!), now much faster (see Job.n_combinations())
def _solve_bruteforce(job: Job) -> tuple[ResultEntry, ...]:
    mutable_job = job.model_copy(deep=True)
    mutable_job.model_config["frozen"] = False

    # allow "overflowing" cut at the end
    # TODO this a simple workaround for singular stocks, remove later
    max_length = mutable_job.stocks[0].length + mutable_job.cut_width

    # find every possible ordering (`factorial(sum(sizes))` elements) and reduce to unique
    all_orderings = set(permutations(mutable_job.iterate_sizes()))

    # start at "all of it"
    minimal_trimmings = mutable_job.n_targets() * max_length
    best_results: list[list[list[NamedSize]]] = []

    # could distribute to multiprocessing, but web worker is parallel anyway
    for combination in all_orderings:
        lengths, trimmings = _group_into_lengths(combination, max_length, mutable_job.cut_width)
        if trimmings < minimal_trimmings:
            minimal_trimmings = trimmings
            best_results.clear()
            best_results.append(lengths)
        elif trimmings == minimal_trimmings:
            best_results.append(lengths)

    # set creates random order of perfect results due to missing sorting, so sort for determinism
    # TODO evaluate which result aligns with user expectations best
    ideal_result = find_best_solution(best_results)
    return sort_entries([create_result_entry(mutable_job.stocks[0], r, mutable_job.cut_width) for r in ideal_result])


def _group_into_lengths(
        combination: tuple[NamedSize, ...], max_length: int, cut_width: int
):
    """
    Collects sizes until length is reached, then starts another stock
    :param combination:
    :param max_length:
    :param cut_width:
    :return:
    """
    stocks: list[list[NamedSize]] = []
    trimmings = 0

    current_size = 0
    current_stock: list[NamedSize] = []
    for size in combination:
        if (current_size + size.length + cut_width) > max_length:
            # start next stock
            stocks.append(current_stock)
            trimmings += _get_trimming(max_length, current_stock, cut_width)
            current_size = 0
            current_stock = []

        current_size += size.length + cut_width
        current_stock.append(size)
    # catch leftovers
    if current_stock:
        stocks.append(current_stock)
        trimmings += _get_trimming(max_length, current_stock, cut_width)
    return stocks, trimmings


# textbook solution, guaranteed to get at most double trimmings of perfect solution; possibly O(n^2)?
def _solve_FFD(job: Job) -> tuple[ResultEntry, ...]:
    # iterate over list of stocks
    # put into first stock that it fits into

    # 1. Sort by magnitude (largest first)
    # 2. stack until limit is reached
    # 3. try smaller as long as possible
    # 4. create new bar

    mutable_sizes = copy.deepcopy(job.required)
    sizes = sorted(mutable_sizes, reverse=True)
    # TODO this a simple workaround for singular stocks, remove later
    max_length = job.stocks[0].length

    stocks: list[list[NamedSize]] = [[]]

    i_target = 0

    while i_target < len(sizes):
        current_size = sizes[i_target]
        for stock in stocks:
            # calculate current stock length
            stock_length = (sum([size.length for size in stock]) + (len(stock) - 1) * job.cut_width)
            # step through existing stocks until current size fits; allow for omitted trailing cut
            if (max_length - stock_length) >= (current_size.length + job.cut_width):
                # add size
                stock.append(current_size.as_base())
                break
        else:  # nothing fit, opening next bin
            stocks.append([current_size.as_base()])

        # decrease/get next
        if current_size.quantity <= 1:
            i_target += 1
        else:
            current_size.quantity -= 1

    return sort_entries([create_result_entry(job.stocks[0], r, job.cut_width) for r in stocks])


# even faster than FFD, seems like equal results; selfmade and less proven!
def _solve_gapfill(job: Job) -> tuple[ResultEntry, ...]:
    # 1. Sort by magnitude (largest first)
    # 2. stack until limit is reached
    # 3. try smaller as long as possible
    # 4. create new bar

    # we are writing around in target sizes, prevent leaking changes to job
    mutable_sizes = copy.deepcopy(job.required)
    targets = sorted(mutable_sizes, reverse=True)
    # TODO this a simple workaround for singular stocks, remove later
    max_length = job.stocks[0].length

    stocks = []

    current_size = 0
    current_stock: list[NamedSize] = []

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
        if (current_size + current_target.length) <= max_length:
            current_stock.append(current_target.as_base())
            current_size += current_target.length
            if current_size < max_length:
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
    return sort_entries([create_result_entry(job.stocks[0], r, job.cut_width) for r in stocks])
