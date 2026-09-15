import pytest
from palindrome import is_palindrome


@pytest.mark.parametrize(
    "number, expected",
    [
        # Одна цифра
#        (0, True), по условию n>0
        (1, True),

        # Две цифры
        (10, False),
        (11, True),
        (55, True),

        # Нечётное количество цифр
        (101, True),
        (121, True),
        (123, False),
        (12321, True),
        (12345, False),

        # Чётное количество цифр
        (1001, True),
        (1221, True),
        (1234, False),
        (1223, False),

        # Нули внутри числа
        (10001, True),
        (10101, True),
        (10201, True),
        (10010, False),

        # Одинаковые цифры
        (111, True),
        (1111, True),
        (99999, True),
    ],
)
def test_is_palindrome(number, expected):
    assert is_palindrome(number) is expected
