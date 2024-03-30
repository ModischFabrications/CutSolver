from typing import Collection

from app.solver.data.Result import ResultLengths


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
