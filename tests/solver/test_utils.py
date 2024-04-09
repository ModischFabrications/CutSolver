import pytest

from app.solver.data.Job import NS
from app.solver.utils import calc_trimming


def test_trimming():
    trimming = calc_trimming(
        stock_length=1500,
        lengths=(NS(length=500), NS(length=500), NS(length=400)),
        cut_width=10,
    )

    assert trimming == 70


def test_trimming_zero():
    trimming = calc_trimming(
        stock_length=1500,
        lengths=(NS(length=500), NS(length=500), NS(length=480)),
        cut_width=10,
    )

    assert trimming == 0


def test_trimming_raise():
    # raises Error if more stock was used than available
    with pytest.raises(OverflowError):
        calc_trimming(1500, (
            NS(length=300),
            NS(length=400),
            NS(length=600),
            NS(length=200)), 2)
