import pytest

from prime import count_primes


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, 0),    #0 и 1 не являются простыми числами
        (1, 0),    #0 и 1 не являются простыми числами
        (2, 0),    # 2 не входит, так как ищем числа < N
        (3, 1),    # единственное простое число — 2
        (4, 2),    # 2 и 3
        (10, 4),   # пример из задания: 2, 3, 5, 7
        (20, 8),   # 2, 3, 5, 7, 11, 13, 17, 19
        (30, 10),  # проверка на большем значении
    ],
)
def test_count_primes(n, expected):
    assert count_primes(n) == expected