#!python3
import copy
from time import perf_counter
from typing import Iterable

from more_itertools import distinct_permutations

from app.settings import solverSettings
from app.solver.data.Job import Job, QNS, NS
from app.solver.data.Result import Result, SolverType, ResultEntry
from app.solver.utils import create_result_entry, sort_entries, find_best_solution


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

    # find every possible ordering (`factorial(sum(sizes))` elements) and reduce to unique
    # equal to set(permutations(...)), but much more efficient
    all_orderings = distinct_permutations(mutable_job.iterate_required())
    all_stocks = distinct_permutations(mutable_job.iterate_stocks())

    # start at "all of it"
    minimal_trimmings: int = sum([stock.length for stock in mutable_job.iterate_stocks()])
    best_results: list[tuple[ResultEntry, ...]] = []

    # could distribute to multiprocessing, but web worker is parallel anyway
    for stock_ordering in all_stocks:
        for required_ordering in all_orderings:
            result = _group_into_lengths(stock_ordering, required_ordering, mutable_job.cut_width)
            if result is None:
                print(".", end="")
                continue
            trimmings = sum(l.trimming for l in result)
            if trimmings < minimal_trimmings:
                minimal_trimmings = trimmings
                best_results.clear()
                best_results.append(result)
            elif trimmings == minimal_trimmings:
                best_results.append(result)

    ideal_result = find_best_solution(best_results)
    return sort_entries([r for r in ideal_result])


def _group_into_lengths(
        stocks: tuple[NS, ...], sizes: Iterable[NS], cut_width: int
) -> tuple[ResultEntry, ...] | None:
    """
    Collects sizes until length is reached, then starts another stock
    Returns none for orderings that exceed ideal conditions
    """
    result: list[ResultEntry] = []
    available = list(reversed(stocks))

    current_size = 0
    current_cuts: list[NS] = []
    current_stock = available.pop()
    for size in sizes:
        if (current_size + size.length) > current_stock.length:
            # start next stock
            result.append(create_result_entry(current_stock, current_cuts, cut_width))
            current_size = 0
            current_cuts = []
            if len(available) <= 0:
                return None
            current_stock = available.pop()

        current_size += size.length + cut_width
        current_cuts.append(size)

    # catch leftovers
    if current_cuts:
        result.append(create_result_entry(current_stock, current_cuts, cut_width))

    return tuple(result)


# textbook solution, guaranteed to get at most double trimmings of perfect solution; possibly O(n^2)?
def _solve_FFD(job: Job) -> tuple[ResultEntry, ...]:
    """
    iterate over list of stocks
    put into first stock that it fits into

    1. Sort by magnitude (largest first)
    2. stack until limit is reached
    3. try smaller as long as possible
    4. create new bar
    """

    mutable_sizes = copy.deepcopy(job.required)
    sizes = sorted(mutable_sizes, reverse=True)
    # TODO this a simple workaround for singular stocks, remove later
    max_length = job.stocks[0].length

    stocks: list[list[NS]] = [[]]

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
    current_stock: list[NS] = []

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

        current_target: QNS = targets[i_target]
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
