from itertools import product

import pytest

from validate_bst import Node, validate_bst


@pytest.mark.parametrize(
    "root, expected",
    [
        (None, True),
        (Node(0), True),
        (Node(2, Node(1)), True),
        (Node(2, right=Node(3)), True),
        (Node(2, Node(3)), False),
        (Node(2, right=Node(1)), False),
        (Node(5, Node(5)), False),
        (Node(5, right=Node(5)), False),
        (Node(0, Node(-10), Node(10)), True),
        (Node(0, Node(-10**100), Node(10**100)), True),
        (Node(8, Node(3, Node(1), Node(6)), Node(10, right=Node(14))), True),
        # Дети локально правильны, но нарушено ограничение корня.
        (Node(8, Node(3, right=Node(9)), Node(10)), False),
        (Node(8, Node(3), Node(10, Node(7))), False),
        # Дубликат предка, а не ближайшего родителя.
        (Node(8, Node(3, right=Node(8))), False),
        (Node(8, right=Node(10, Node(8))), False),
        # Значения в допустимых интервалах, дерево не обязано быть полным.
        (Node(8, Node(3, right=Node(7)), Node(10, Node(9))), True),
    ],
)
def test_validate_bst(root, expected):
    assert validate_bst(root) is expected


def test_no_mutation_and_repeated_calls():
    left = Node(1)
    right = Node(3)
    root = Node(2, left, right)
    for _ in range(2):
        assert validate_bst(root) is True
        assert (root.value, root.left, root.right) == (2, left, right)
        assert (left.value, left.left, left.right) == (1, None, None)
        assert (right.value, right.left, right.right) == (3, None, None)
    right.left = Node(0)
    assert validate_bst(root) is False
    assert right.left.value == 0


@pytest.mark.parametrize("side", ["left", "right"])
def test_deep_chain(side):
    root = Node(0)
    node = root
    direction = -1 if side == "left" else 1
    for i in range(1, 5_000):
        child = Node(direction * i)
        setattr(node, side, child)
        node = child
    assert validate_bst(root) is True
    # Ошибка обнаруживается только на самом глубоком уровне.
    node.value = 0
    assert validate_bst(root) is False


def test_many_values_against_inorder_criterion():
    # Для строгого BST inorder должен быть строго возрастающим.
    # Проверяем все 3125 наборов, включая корректный и варианты с дубликатами.
    for a, b, c, d, e in product(range(5), repeat=5):
        root = Node(a, Node(b, right=Node(c)), Node(d, Node(e)))
        inorder = [b, c, a, e, d]
        expected = all(x < y for x, y in zip(inorder, inorder[1:]))
        assert validate_bst(root) is expected


def test_large_balanced_tree():
    def build(start, stop):
        if start >= stop:
            return None
        middle = (start + stop) // 2
        return Node(middle, build(start, middle), build(middle + 1, stop))

    assert validate_bst(build(0, 16_383)) is True
