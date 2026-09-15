import pytest

from sum import max_even_sum


@pytest.mark.parametrize(
    "numbers, expected",
    [
        # Сумма уже чётная
        ([2, 4, 6], 12),

        # Одно чётное число
        ([8], 8),

        # Одно нечётное число
        ([3], 0),

        # Сумма нечётная, одно нечётное число
        ([1, 2, 4], 6),

        # Сумма нечётная, несколько нечётных —
        # выбираем минимальное
        ([5, 7, 3, 2], 14),

        # Только нечётные, количество чётное
        ([1, 3], 4),

        # Только нечётные, количество нечётное
        ([1, 3, 5], 8),
    ],
)
def test_max_even_sum(numbers, expected):
    assert max_even_sum(numbers) == expected