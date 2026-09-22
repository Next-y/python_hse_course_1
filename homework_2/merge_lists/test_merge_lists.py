import pytest

from merge_lists import Node, merge_with_dummy, merge_without_dummy


def build_list(values):
    #Построить входной список и сохранить его узлы для проверки результата
    head = None
    tail = None
    nodes = []

    for value in values:
        node = Node(value)
        nodes.append(node)

        if head is None:
            head = node
        else:
            tail.next = node

        tail = node

    return head, nodes


def check_result(head, expected_values):
    """Проверить значения и их порядок в результирующем списке."""
    values = []
    current = head

    while current is not None:
        values.append(current.value)
        current = current.next

    assert values == expected_values


@pytest.mark.parametrize("merge", [merge_with_dummy, merge_without_dummy])
@pytest.mark.parametrize(
    "values1, values2, expected",
    [
        ([], [], []),
        ([], [1], [1]),
        ([1], [], [1]),
        ([], [-3, 0, 7], [-3, 0, 7]),
        ([-3, 0, 7], [], [-3, 0, 7]),
        ([1], [2], [1, 2]),
        ([2], [1], [1, 2]),
        ([0], [0], [0, 0]),
        ([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),
        ([1, 3, 5], [2, 4, 6], [1, 2, 3, 4, 5, 6]),
        ([2, 4, 6], [1, 3, 5], [1, 2, 3, 4, 5, 6]),
        ([1, 2], [3, 4, 5], [1, 2, 3, 4, 5]),
        ([3, 4, 5], [1, 2], [1, 2, 3, 4, 5]),
        ([2, 2, 2], [2, 2], [2, 2, 2, 2, 2]),
        ([-5, -2], [-4, -3, -1], [-5, -4, -3, -2, -1]),
        ([-1, 3, 8], [-4, 0, 3, 5], [-4, -1, 0, 3, 3, 5, 8]),
        ([4], [-2, 0, 1, 4, 7, 9], [-2, 0, 1, 4, 4, 7, 9]),
        ([-2, 0, 1, 4, 7, 9], [4], [-2, 0, 1, 4, 4, 7, 9]),
    ],
)
def test_merge(merge, values1, values2, expected):
    list1, _ = build_list(values1)
    list2, _ = build_list(values2)

    result = merge(list1, list2)

    check_result(result, expected)


@pytest.mark.parametrize("merge", [merge_with_dummy, merge_without_dummy])
def test_merge_returns_existing_head_when_one_list_is_empty(merge):
    head, _ = build_list([-2, 0, 3])

    assert merge(None, head) is head
    assert merge(head, None) is head
    check_result(head, [-2, 0, 3])


@pytest.mark.parametrize("merge", [merge_with_dummy, merge_without_dummy])
def test_equal_values_keep_original_order(merge):
    list1, nodes1 = build_list([2, 2])
    list2, nodes2 = build_list([2, 2])

    current = merge(list1, list2)

    # При равных головах реализация выбирает первый список (сравнение <=).
    for node in nodes1 + nodes2:
        assert current is node
        current = current.next

    assert current is None


@pytest.mark.parametrize("merge", [merge_with_dummy, merge_without_dummy])
def test_merge_long_lists(merge):
    # 100 000 узлов
    list1, _ = build_list(range(0, 100_000, 2))
    list2, _ = build_list(range(1, 100_000, 2))

    result = merge(list1, list2)

    check_result(result, list(range(100_000)))
