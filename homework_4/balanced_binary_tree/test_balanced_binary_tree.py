import pytest

from balanced_binary_tree import Node, is_balanced


@pytest.mark.parametrize(
    "root, expected",
    [
        (None, True),
        (Node(0), True),
        (Node(1, Node(2)), True),
        (Node(1, right=Node(2)), True),
        (Node(1, Node(2, Node(3))), False),
        (Node(1, right=Node(2, right=Node(3))), False),
        (Node(1, Node(2, right=Node(3))), False),
        (Node(8, Node(3, Node(1), Node(6)), Node(10)), True),
        # Баланс не зависит от BST или уникальности значений.
        (Node(0, Node(10), Node(-10)), True),
        (Node(5, Node(5), Node(5)), True),
        # Корень сбалансирован, но один из потомков — нет.
        (Node(8, Node(3, Node(2, Node(1))), Node(10, right=Node(11))), False),
        (Node(8, Node(3, Node(2)), Node(10, right=Node(11, right=Node(12)))), False),
        # Одинаковая высота ветвей корня не скрывает нарушение внутри них.
        (Node(0, Node(1, Node(2, Node(3))), Node(4, right=Node(5, right=Node(6)))), False),
    ],
)
def test_is_balanced(root, expected):
    assert is_balanced(root) is expected


def test_no_mutation_and_repeated_calls():
    left, right = Node(2), Node(3)
    root = Node(1, left, right)
    for _ in range(2):
        assert is_balanced(root) is True
        assert (root.value, root.left, root.right) == (1, left, right)
        assert (left.value, left.left, left.right) == (2, None, None)
        assert (right.value, right.left, right.right) == (3, None, None)
    left.left = Node(4, Node(5))
    assert is_balanced(root) is False
    assert left.left.left.value == 5


@pytest.mark.parametrize("side", ["left", "right"])
def test_deep_chain(side):
    root = Node(0)
    node = root
    for value in range(1, 5_000):
        child = Node(value)
        setattr(node, side, child)
        node = child
    assert is_balanced(root) is False


def test_large_complete_tree():
    # 16 383 узла; в каждом узле высоты двух ветвей одинаковы.
    def build(height):
        if height == 0:
            return None
        return Node(0, build(height - 1), build(height - 1))

    assert is_balanced(build(14)) is True


def test_all_small_tree_shapes_against_simple_reference():
    # Эталон намеренно считает высоты заново: медленно, но просто.
    # Все формы до 7 узлов включают 626 деревьев, вместе с пустым.
    def height(node):
        if node is None:
            return 0
        return 1 + max(height(node.left), height(node.right))

    def reference(node):
        if node is None:
            return True
        return (abs(height(node.left) - height(node.right)) <= 1
                and reference(node.left) and reference(node.right))

    def shapes(size):
        if size == 0:
            return [None]
        result = []
        for left_size in range(size):
            for left in shapes(left_size):
                for right in shapes(size - left_size - 1):
                    result.append((left, right))
        return result

    def build(shape):
        if shape is None:
            return None
        return Node(0, build(shape[0]), build(shape[1]))

    for size in range(8):
        for shape in shapes(size):
            root = build(shape)
            assert is_balanced(root) is reference(root)
