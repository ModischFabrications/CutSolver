import pytest

from app.solver.data.Job import NamedSize
from app.solver.utils import _get_trimming


def test_trimming():
    trimming = _get_trimming(
        stock_length=1500,
        lengths=(NamedSize(length=500), NamedSize(length=500), NamedSize(length=400)),
        cut_width=10,
    )

    assert trimming == 70


def test_trimming_zero():
    trimming = _get_trimming(
        stock_length=1500,
        lengths=(NamedSize(length=500), NamedSize(length=500), NamedSize(length=480)),
        cut_width=10,
    )

    assert trimming == 0


def test_trimming_raise():
    # raises Error if more stock was used than available
    with pytest.raises(OverflowError):
        _get_trimming(1500, (
            NamedSize(length=300),
            NamedSize(length=400),
            NamedSize(length=600),
            NamedSize(length=200)), 2)
