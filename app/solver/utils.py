from typing import Collection, Sequence

from app.solver.data.Job import NS
from app.solver.data.Result import ResultEntry


def _get_trimming(stock_length: int, lengths: Collection[NS], cut_width: int) -> int:
    sum_lengths = sum([size.length for size in lengths])
    sum_cuts = len(lengths) * cut_width

    trimmings = stock_length - (sum_lengths + sum_cuts)

    # cut at the end can be omitted
    if trimmings == -cut_width:
        trimmings = 0

    if trimmings < 0:
        raise OverflowError("Trimmings can't ever be negative!")

    return trimmings


def find_best_solution(solutions: Sequence):
    # TODO evaluate which one aligns with user expectations best (see #68)
    # always sort for determinism!
    return sorted(solutions, reverse=True)[0]


def create_result_entry(stock: NS, cuts: list[NS], cut_width: int) -> ResultEntry:
    return ResultEntry(
        stock=stock,
        cuts=tuple(sorted(cuts, reverse=True)),
        trimming=_get_trimming(stock.length, cuts, cut_width)
    )


def sort_entries(result_entries: list[ResultEntry]) -> tuple[ResultEntry, ...]:
    return tuple(sorted(result_entries))
