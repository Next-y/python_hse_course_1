from itertools import permutations

import pytest

from tree_traversal import BST, Node


ORDERS = [
    "preorder", "inorder", "postorder", "reverse_preorder",
    "reverse_inorder", "reverse_postorder",
]


def make_tree(values):
    tree = BST()
    for value in values:
        assert tree.insert(value) is None
    return tree


def snapshot(root):
    # Снимок значений и ссылок, чтобы заметить изменение дерева обходом.
    result = []
    stack = [root] if root is not None else []
    while stack:
        node = stack.pop()
        result.append((node, node.value, node.left, node.right))
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return result


@pytest.mark.parametrize("method", ORDERS)
@pytest.mark.parametrize("values, expected", [([], []), ([0], [0]), ([5, 5], [5])])
def test_empty_single_and_duplicate(method, values, expected):
    tree = make_tree(values)
    assert getattr(tree, method)() == expected


@pytest.mark.parametrize(
    "method, expected",
    [
        ("preorder", [8, 3, 1, 6, 4, 7, 10, 14, 13]),
        ("inorder", [1, 3, 4, 6, 7, 8, 10, 13, 14]),
        ("postorder", [1, 4, 7, 6, 3, 13, 14, 10, 8]),
        ("reverse_preorder", [8, 10, 14, 13, 3, 6, 7, 4, 1]),
        ("reverse_inorder", [14, 13, 10, 8, 7, 6, 4, 3, 1]),
        ("reverse_postorder", [13, 14, 10, 7, 4, 6, 1, 3, 8]),
    ],
)
def test_visualization_and_no_mutation(method, expected):
    tree = make_tree([8, 3, 10, 1, 6, 14, 4, 7, 13])
    before = snapshot(tree.root)
    result = getattr(tree, method)()
    assert type(result) is list
    assert result == expected
    assert snapshot(tree.root) == before
    # Результаты независимы, изменение списка не затрагивает дерево.
    result.append(999)
    assert getattr(tree, method)() == expected
    assert snapshot(tree.root) == before


def test_insertion_structure_and_duplicates():
    tree = make_tree([8, 3, 10, 1, 6, 14, 4, 7, 13])
    assert tree.root.value == 8
    assert tree.root.left.value == 3
    assert tree.root.right.value == 10
    assert tree.root.left.left.value == 1
    assert tree.root.left.right.value == 6
    assert tree.root.left.right.left.value == 4
    assert tree.root.left.right.right.value == 7
    assert tree.root.right.left is None
    assert tree.root.right.right.value == 14
    assert tree.root.right.right.left.value == 13
    before = snapshot(tree.root)
    for value in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
        tree.insert(value)
    assert snapshot(tree.root) == before


@pytest.mark.parametrize("values", [
    [0, -5, 5, -10, -1, 1, 10, 0, -5],
    [10**100, 0, -10**100, 10**100],
    list(range(100)),
    list(range(100, -1, -1)),
])
def test_sorted_output(values):
    tree = make_tree(values)
    assert tree.inorder() == sorted(set(values))
    assert tree.reverse_inorder() == sorted(set(values), reverse=True)


def test_all_small_insertion_orders():
    for values in permutations([-2, -1, 0, 1, 2]):
        tree = make_tree(values)
        assert tree.inorder() == [-2, -1, 0, 1, 2]
        # Независимая проверка: все потомки слева/справа удовлетворяют BST.
        for node, value, left, right in snapshot(tree.root):
            assert all(item[1] < value for item in snapshot(left))
            assert all(item[1] > value for item in snapshot(right))


@pytest.mark.parametrize("side", ["left", "right"])
@pytest.mark.parametrize("method", ORDERS)
def test_deep_chain(side, method):
    # Создаём цепочку напрямую за O(n), затем отдельно проверяем insert.
    n = 5_000
    values = list(range(n)) if side == "right" else list(range(n, 0, -1))
    tree = BST()
    tree.root = Node(values[0])
    node = tree.root
    for value in values[1:]:
        child = Node(value)
        setattr(node, side, child)
        node = child
    extra = n if side == "right" else 0
    tree.insert(extra)
    assert getattr(node, side).value == extra
    values.append(extra)
    if method in ["postorder", "reverse_postorder"]:
        expected = values[::-1]
    elif method == "inorder":
        expected = sorted(values)
    elif method == "reverse_inorder":
        expected = sorted(values, reverse=True)
    else:
        expected = values
    assert getattr(tree, method)() == expected
