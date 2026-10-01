import pytest

from anagrams import anagrams


def normalize(groups):
    # Сравниваем состав групп независимо от порядка, сохраняя все повторы.
    return sorted(tuple(sorted(group)) for group in groups)


@pytest.mark.parametrize(
    "strs, expected",
    [
        (
            ["eat", "tea", "tan", "ate", "nat", "bat"],
            [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]],
        ),
        ([], []),                                  # Пустой список
        (["word"], [["word"]]),                    # Одно слово
        ([""], [[""]]),                            # Пустое слово
        (["", "a", ""], [["", ""], ["a"]]),         # Несколько пустых слов
        (["a", "b", "a"], [["a", "a"], ["b"]]),     # Однобуквенные слова
        (["cat", "dog", "sun"], [["cat"], ["dog"], ["sun"]]),
        (["abc", "bca", "cab"], [["abc", "bca", "cab"]]),
        (["ab", "aab", "baa"], [["ab"], ["aab", "baa"]]),
        (["aa", "aa", "aa"], [["aa", "aa", "aa"]]),
        (
            ["aab", "tea", "aba", "ab", "eat", "aab"],
            [["aab", "aba", "aab"], ["tea", "eat"], ["ab"]],
        ),
        (["кот", "ток", "кто", "кит"], [["кот", "ток", "кто"], ["кит"]]),
        (["Ab", "bA", "ab", "ba"], [["Ab", "bA"], ["ab", "ba"]]),
        (["a!", "!a", "a ", " a", "a"], [["a!", "!a"], ["a ", " a"], ["a"]])
    ],
)
def test_anagrams(strs, expected):
    strs_before = strs.copy()

    result = anagrams(strs)

    assert normalize(result) == normalize(expected)
    assert strs == strs_before


def test_anagrams_long_words():
    first = "a" * 10_000 + "б" * 10_000
    second = "б" * 10_000 + "a" * 10_000
    different = "a" * 10_001 + "б" * 9_999

    assert normalize(anagrams([first, different, second])) == normalize(
        [[first, second], [different]]
    )


def test_anagrams_many_words():
    strs = ["ab", "ba", "xyz", "zyx", ""] * 2_000
    expected = [["ab", "ba"] * 2_000, ["xyz", "zyx"] * 2_000, [""] * 2_000]

    assert normalize(anagrams(strs)) == normalize(expected)
