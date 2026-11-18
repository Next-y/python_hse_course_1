import pytest

from iterative import mergesort, quicksort


@pytest.mark.parametrize("nums, expected", [
    ([], []),
    ([1], [1]),
    ([6, 2, 5, 3, 1, 4, 3], [1, 2, 3, 3, 4, 5, 6]),
    ([2, 2, 2, 2], [2, 2, 2, 2]),
    ([-4, -1, 0, 3, 8], [-4, -1, 0, 3, 8]),
    ([6, 5, 4, 3, 2, 1, 0, -1], [-1, 0, 1, 2, 3, 4, 5, 6]),
])
def test_sorts(nums, expected):
    before = nums.copy()
    for sort in (mergesort, quicksort):
        result = sort(nums)
        assert result == expected
        assert result is not nums
        assert nums == before
