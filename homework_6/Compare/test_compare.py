import pytest

from compare import mergesort, quicksort, timed


@pytest.mark.parametrize("nums, expected", [
    ([], []),
    ([8], [8]),
    ([4, 1, 3, 1, 2], [1, 1, 2, 3, 4]),
    ([2, 1, 0, -1], [-1, 0, 1, 2]),
    (list(range(1200)), list(range(1200))),
    ([7] * 8, [7] * 8),
])
def test_sorts(nums, expected):
    before = nums.copy()
    for sort in (mergesort, quicksort):
        result = sort(nums)
        assert result == expected
        assert result is not nums
        assert nums == before


def test_timer(monkeypatch):
    ticks = iter([100, 145])
    monkeypatch.setattr("compare.perf_counter_ns", lambda: next(ticks))

    @timed
    def multiply(x, *, factor):
        return x * factor

    assert multiply(4, factor=2) == (8, 45)
