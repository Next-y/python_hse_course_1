from itertools import permutations as reference_permutations, product
from math import factorial

import pytest

from permutations.permute import permutations


@pytest.mark.parametrize("nums, expected", [
    ([1, 2, 3], [[1, 2, 3], [1, 3, 2], [2, 1, 3],
                 [2, 3, 1], [3, 1, 2], [3, 2, 1]]),
    ([0, 1], [[0, 1], [1, 0]]),
    ([1], [[1]]),
    ([], [[]]),
    ([0], [[0]]),
    ([2, 1], [[2, 1], [1, 2]]),
    ([1, 1, 2], [[1, 1, 2], [1, 2, 1], [2, 1, 1]]),
    ([2, 1, 2], [[2, 2, 1], [2, 1, 2], [1, 2, 2]]),
    ([5, 5, 5], [[5, 5, 5]]),
    ([-1, 0], [[-1, 0], [0, -1]]),
])
@pytest.mark.parametrize("trace", [False, True])
def test_examples_and_boundaries(nums, expected, trace, capsys):
    before = nums.copy()
    assert permutations(nums, trace=trace) == expected
    assert nums == before
    output = capsys.readouterr().out
    if trace:
        assert output.startswith("-> backtrack([])\n")
        assert output.endswith(f"<- backtrack = {len(expected)}\n")
    else:
        assert output == ""


def test_default_trace_shows_complete_stack(capsys):
    assert permutations([0, 1]) == [[0, 1], [1, 0]]
    assert capsys.readouterr().out.splitlines() == [
        "-> backtrack([])",
        "  -> backtrack([0])",
        "    -> backtrack([0, 1])",
        "    <- backtrack = 1",
        "  <- backtrack = 1",
        "  -> backtrack([1])",
        "    -> backtrack([1, 0])",
        "    <- backtrack = 1",
        "  <- backtrack = 1",
        "<- backtrack = 2",
    ]


def test_empty_trace_and_repeated_calls(capsys):
    for _ in range(2):
        assert permutations([]) == [[]]
        assert capsys.readouterr().out == "-> backtrack([])\n<- backtrack = 1\n"


def test_results_are_independent_lists():
    nums = [1, 2, 3]
    result = permutations(nums, trace=False)
    assert type(result) is list
    assert all(type(row) is list and row is not nums for row in result)
    assert len({id(row) for row in result}) == 6
    result[0][0] = 999
    result[1].append(100)
    assert result[2:] == [[2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    assert nums == [1, 2, 3]
    assert permutations(nums, trace=False)[0] == [1, 2, 3]


def test_all_short_inputs_against_standard_library():
    # Включает все сочетания повторов; эталон не использует наш алгоритм.
    for size in range(6):
        for values in product([-1, 0, 1], repeat=size):
            nums = list(values)
            result = permutations(nums, trace=False)
            actual = [tuple(row) for row in result]
            expected = set(reference_permutations(nums))
            assert set(actual) == expected
            assert len(actual) == len(expected)
            assert nums == list(values)


@pytest.mark.parametrize("nums", [
    list(range(7)),
    [2, 1, 2, 1, 0, 0],
    [-10**100, 0, 10**100],
    [7] * 50,
])
def test_larger_and_unusual_inputs(nums):
    result = permutations(nums, trace=False)
    expected_count = factorial(len(nums))
    for value in set(nums):
        expected_count //= factorial(nums.count(value))
    assert len(result) == expected_count
    assert len({tuple(row) for row in result}) == expected_count
    assert all(sorted(row) == sorted(nums) for row in result)
