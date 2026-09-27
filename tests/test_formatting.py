import pytest

from italian_champions_results.formatting import format_time


@pytest.mark.parametrize(
    "seconds,expected",
    [(None, "-"), (59, "0:59"), (1127, "18:47"), (10367, "2:52:47")],
)
def test_format_time(seconds, expected):
    assert format_time(seconds) == expected
