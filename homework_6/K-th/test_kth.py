import pytest

from kth import find_kth_largest


@pytest.mark.parametrize("nums, k, expected", [
    ([3, 2, 1, 5, 6, 4], 2, 5),
    ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),
    ([8], 1, 8),
    ([1, 4, 2], 1, 4),
    ([-5, -2, -2], 3, -5),
    ([9, 7, 2, 7, 7], 3, 7),
    ([4, 4, 4, 4], 2, 4),
])
def test_kth(nums, k, expected):
    before = nums.copy()
    assert find_kth_largest(nums, k) == expected
    assert nums == before


@pytest.mark.parametrize("nums, k", [([], 1), ([2, 1], 0), ([2, 1], 3)])
def test_rank_out_of_range(nums, k):
    with pytest.raises(ValueError):
        find_kth_largest(nums, k)


def test_fractional_rank():
    with pytest.raises(TypeError):
        find_kth_largest([2, 1], 1.5)
