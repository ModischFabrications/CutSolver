#!python3
import copy
from time import perf_counter

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
    elif job.n_entries() <= solverSettings.solver_n_max:
        layout = _solve_FFD(job)
        solver_type = SolverType.FFD
    else:
        raise OverflowError("Input too large")

    time_us = int((perf_counter() - time) * 1000 * 1000)

    return Result(job=job, solver_type=solver_type, time_us=time_us, layout=layout)


# slowest, but perfect solver; originally O(n!), now much faster (see Job.n_combinations())
def _solve_bruteforce(job: Job) -> tuple[ResultEntry, ...]:
    minimal_trimmings = float('inf')
    best_results = []

    required_orderings = distinct_permutations(job.iterate_required())
    for stock_ordering in distinct_permutations(job.iterate_stocks()):
        for required_ordering in required_orderings:
            result = _group_into_lengths(stock_ordering, required_ordering, job.cut_width)
            if result is None:
                # Short-circuit if bad solution
                continue
            trimmings = sum(lt.trimming for lt in result)
            if trimmings < minimal_trimmings:
                minimal_trimmings = trimmings
                best_results = [result]
            elif trimmings == minimal_trimmings:
                best_results.append(result)

    assert best_results, "No valid solution found"
    return sort_entries(find_best_solution(best_results))


def _group_into_lengths(stocks: tuple[NS, ...], sizes: tuple[NS, ...], cut_width: int) \
        -> tuple[ResultEntry, ...] | None:
    """
    Collects sizes until length is reached, then starts another stock
    Returns None for orderings that exceed ideal conditions
    """
    available = list(reversed(stocks))
    required = list(reversed(sizes))

    result: list[ResultEntry] = []
    current_cuts: list[NS] = []
    cut_sum = 0  # could be calculated, but I think this is faster

    current_stock = available.pop()
    size = required.pop()
    for _ in range(999):
        while (cut_sum + size.length) <= current_stock.length:
            cut_sum += size.length + cut_width
            current_cuts.append(size)

            if len(required) <= 0:
                # we are done here
                result.append(create_result_entry(current_stock, current_cuts, cut_width))
                return tuple(result)

            size = required.pop()
            continue

        # short stocks will simply be skipped
        if len(current_cuts) > 0:
            result.append(create_result_entry(current_stock, current_cuts, cut_width))
            cut_sum = 0
            current_cuts.clear()

        if len(available) <= 0:
            # our solution is shit, we can cancel
            return None
        current_stock = available.pop()

    raise OverflowError("_group_into_lengths had an infinite loop, cancelling...")


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
    stocks = sorted(mutable_sizes, reverse=True)
    # TODO this a simple workaround for singular stocks, remove later
    max_length = job.stocks[0].length

    layout: list[list[NS]] = [[]]

    i_size = 0

    while i_size < len(sizes):
        current_size = sizes[i_size]
        for stock in layout:
            # calculate current stock length
            stock_length = (sum([size.length for size in stock]) + (len(stock) - 1) * job.cut_width)
            # step through existing stocks until current size fits; allow for omitted trailing cut
            if (current_size.length + stock_length + job.cut_width) <= max_length:
                stock.append(current_size.as_base())
                break
        else:  # nothing fit, opening next bin
            layout.append([current_size.as_base()])

        # decrease/get next
        if current_size.quantity <= 1:
            i_size += 1
        else:
            current_size.quantity -= 1

    # TODO use right stock
    return sort_entries([create_result_entry(job.stocks[0].as_base(), r, job.cut_width) for r in layout])


# even faster than FFD, seems like equal results; self-made and less proven!
def _solve_gapfill(job: Job) -> tuple[ResultEntry, ...]:
    """
    1. Sort by magnitude (largest first)
    2. stack until limit is reached
    3. try smaller as long as possible
    4. create new bar
    """

    # we are writing around in target sizes, prevent leaking changes to job
    mutable_sizes = copy.deepcopy(job.required)
    targets = sorted(mutable_sizes, reverse=True)
    # TODO this a simple workaround for singular stocks, remove later
    max_length = job.stocks[0].length
    stocks = sorted(job.iterate_stocks(), reverse=True)

    cuts = []

    current_size = 0
    current_stock: list[NS] = []

    i_target = 0
    while len(targets) > 0:
        # nothing fit, next stock
        if i_target >= len(targets):
            # add local result
            cuts.append(current_stock)

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
        cuts.append(current_stock)

    # TODO use right stock
    # trimming could be calculated from len(stocks) * length - sum(stocks)
    return sort_entries([create_result_entry(job.stocks[0].as_base(), r, job.cut_width) for r in cuts])
