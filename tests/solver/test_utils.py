import pytest

from app.solver.utils import _get_trimming, _get_trimmings


def test_trimming():
    trimming = _get_trimming(
        max_length=1500,
        lengths=((500, ""), (500, ""), (400, "")),
        cut_width=10,
    )

    assert trimming == 70


def test_trimming_zero():
    trimming = _get_trimming(
        max_length=1500,
        lengths=((500, ""), (500, ""), (480, "")),
        cut_width=10,
    )

    assert trimming == 0


def test_trimming_raise():
    # raises Error if more stock was used than available
    with pytest.raises(OverflowError):
        _get_trimming(1500, ((300, ""), (400, ""), (600, ""), (200, "")), 2)


def test_trimmings():
    trimming = _get_trimmings(
        max_length=1500,
        lengths=(((500, ""), (500, ""), (400, "")), ((500, ""), (500, ""), (400, ""))),
        cut_width=10,
    )

    assert trimming == 140
