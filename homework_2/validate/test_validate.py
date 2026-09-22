import pytest

from validate import validate


@pytest.mark.parametrize(
    "pushed, popped, expected",
    [
        ([1], [1], True),                           # Минимальная длина
        ([0], [0], True),                           # Ноль
        ([1, 2], [1, 2], True),                     # Сразу извлекаем
        ([1, 2], [2, 1], True),                     # Сначала добавляем все
        ([1, 2, 3, 4, 5], [1, 3, 5, 4, 2], True),  # Пример из условия
        ([1, 2, 3], [3, 1, 2], False),              # Пример из условия
        ([1, 2, 3, 4], [1, 2, 3, 4], True),
        ([1, 2, 3, 4], [4, 3, 2, 1], True),
        ([1, 2, 3, 4, 5], [2, 1, 4, 3, 5], True),  # Стек опустошается повторно
        ([1, 2, 3, 4, 5], [2, 4, 5, 3, 1], True),  # Вложенные извлечения
        ([1, 2, 3, 4, 5], [1, 5, 2, 4, 3], False),
        ([1, 2, 3, 4, 5], [4, 2, 3, 5, 1], False),
        ([-3, 0, 5, -1], [0, -1, 5, -3], True),    # Разные знаки
        ([-3, 0, 5], [5, -3, 0], False),
        ([10, -5, 8, 0], [-5, 0, 8, 10], True),    # pushed не отсортирована
        ([2, 4, 6, 8, 10, 12], [4, 8, 6, 12, 10, 2], True),
        ([2, 4, 6, 8, 10, 12], [4, 8, 2, 12, 10, 6], False),
    ],
)
def test_validate(pushed, popped, expected):
    pushed_before = pushed.copy()
    popped_before = popped.copy()

    assert validate(pushed, popped) is expected
    assert pushed == pushed_before
    assert popped == popped_before


@pytest.mark.parametrize("order", ["same", "reverse", "blocked"])
def test_validate_maximum_length(order):
    pushed = list(range(100_000))

    if order == "same":
        popped = pushed.copy()
        expected = True
    elif order == "reverse":
        popped = pushed[::-1]
        expected = True
    else:
        # После извлечения 99 999 требуется 0, но сверху находится 99 998.
        popped = [99_999] + list(range(99_999))
        expected = False

    assert validate(pushed, popped) is expected
