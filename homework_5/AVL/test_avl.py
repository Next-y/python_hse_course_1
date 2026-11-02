from itertools import permutations
from random import Random

import pytest

from AVL.avl import AVL


def assert_avl(tree, expected):
    # Независимо пересчитываем высоты и проверяем ограничения ВСЕХ предков.
    seen = set()
    values = []

    def check(node, lower=None, upper=None):
        if node is None:
            return 0
        assert id(node) not in seen, "Цикл или общий узел у двух поддеревьев"
        seen.add(id(node))
        assert lower is None or lower < node.value
        assert upper is None or node.value < upper
        left_height = check(node.left, lower, node.value)
        values.append(node.value)
        right_height = check(node.right, node.value, upper)
        actual_height = 1 + max(left_height, right_height)
        assert node.height == actual_height
        assert abs(left_height - right_height) <= 1
        return actual_height

    check(tree.root)
    assert values == sorted(expected)
    assert tree.inorder() == values


def make_tree(values):
    tree = AVL()
    expected = set()
    for value in values:
        assert tree.insert(value) is None
        expected.add(value)
        assert_avl(tree, expected)
    return tree


def snapshot(node):
    if node is None:
        return None
    return (id(node), node.value, node.height,
            snapshot(node.left), snapshot(node.right))


def test_empty_tree():
    tree = AVL()
    assert tree.root is None
    assert tree.search(0) is False
    assert tree.delete(0) is None
    assert tree.visualize() == "root: ∅"
    assert_avl(tree, [])


@pytest.mark.parametrize("value", [0, -10, 10**100, -10**100])
def test_single_node_duplicate_delete_and_reuse(value):
    tree = make_tree([value])
    assert tree.search(value) is True
    before = snapshot(tree.root)
    assert tree.insert(value) is None
    assert tree.delete(value + 1) is None
    assert tree.search(value + 1) is False
    assert snapshot(tree.root) == before
    assert tree.delete(value) is None
    assert tree.root is None
    assert tree.search(value) is False
    assert tree.delete(value) is None
    tree.insert(value)
    assert_avl(tree, [value])


@pytest.mark.parametrize("values", [
    [30, 20, 10],  # LL
    [10, 20, 30],  # RR
    [30, 10, 20],  # LR
    [10, 30, 20],  # RL
])
def test_all_four_insertion_rotations(values):
    tree = make_tree(values)
    assert tree.root.value == 20
    assert tree.root.left.value == 10
    assert tree.root.right.value == 30
    assert_avl(tree, [10, 20, 30])


@pytest.mark.parametrize("values, deleted, root", [
    ([4, 2, 5, 1], 5, 2),        # LL, баланс ребёнка 1
    ([2, 1, 4, 5], 1, 4),        # RR, баланс ребёнка -1
    ([5, 2, 7, 4], 7, 4),        # LR
    ([3, 1, 6, 4], 1, 4),        # RL
    ([4, 2, 5, 1, 3], 5, 2),     # LL, баланс ребёнка 0
    ([2, 1, 4, 3, 5], 1, 4),     # RR, баланс ребёнка 0
])
def test_deletion_rotations(values, deleted, root):
    tree = make_tree(values)
    tree.delete(deleted)
    assert tree.root.value == root
    assert tree.search(deleted) is False
    assert_avl(tree, set(values) - {deleted})


@pytest.mark.parametrize("values, deleted", [
    ([2, 1, 3], 1),                        # Лист
    ([2, 1], 2),                           # Корень с левым ребёнком
    ([2, 3], 2),                           # Корень с правым ребёнком
    ([4, 2, 6, 1], 2),                     # Внутренний узел с ребёнком
    ([4, 2, 6, 7], 6),                     # Ребёнок справа
    ([2, 1, 3], 2),                        # Два ребёнка, successor рядом
    ([4, 2, 6, 1, 3, 5, 7], 4),           # Successor глубже справа
    ([20, 10, 40, 5, 15, 30, 50, 35], 20), # У successor есть ребёнок
])
def test_deletion_structural_cases(values, deleted):
    tree = make_tree(values)
    tree.delete(deleted)
    remaining = set(values) - {deleted}
    assert_avl(tree, remaining)
    assert tree.search(deleted) is False
    for value in remaining:
        assert tree.search(value) is True


def test_visualization_example_and_read_only_operations():
    tree = make_tree([30, 10, 20, 40, 50, 25])
    assert tree.root.value == 30
    assert tree.root.left.value == 20
    assert tree.root.right.value == 40
    assert tree.root.left.right.value == 25
    tree.delete(30)
    assert tree.root.value == 40
    assert_avl(tree, [10, 20, 25, 40, 50])
    tree.delete(50)
    assert_avl(tree, [10, 20, 25, 40])
    before = snapshot(tree.root)
    assert tree.visualize() == "\n".join([
        "root: 20 [h=3, b=-1]",
        "    L: 10 [h=1, b=0]",
        "    R: 40 [h=2, b=1]",
        "        L: 25 [h=1, b=0]",
        "        R: ∅",
    ])
    assert tree.search(25) is True
    assert tree.search(35) is False
    result = tree.inorder()
    result.append(999)
    assert tree.inorder() == [10, 20, 25, 40]
    for value in [10, 20, 25, 40]:
        tree.insert(value)
    tree.delete(999)
    assert snapshot(tree.root) == before


def test_independent_trees():
    first = make_tree([2, 1, 3])
    second = make_tree([10])
    first.delete(2)
    second.insert(20)
    assert_avl(first, [1, 3])
    assert_avl(second, [10, 20])


def test_all_small_insertion_and_deletion_orders():
    # Все 24 * 24 сочетания порядков; инварианты проверяем после каждой операции.
    orders = list(permutations(range(4)))
    for insertion_order in orders:
        for deletion_order in orders:
            tree = make_tree(insertion_order)
            expected = set(insertion_order)
            for value in deletion_order:
                tree.delete(value)
                expected.remove(value)
                assert_avl(tree, expected)
            assert tree.root is None


@pytest.mark.parametrize("seed", [0, 17, 2026])
def test_mixed_operations_against_set(seed):
    rng = Random(seed)
    tree = AVL()
    expected = set()
    for _ in range(1_000):
        value = rng.randrange(-100, 101)
        operation = rng.choice(["insert", "delete", "search"])
        if operation == "insert":
            tree.insert(value)
            expected.add(value)
        elif operation == "delete":
            tree.delete(value)
            expected.discard(value)
        else:
            before = snapshot(tree.root)
            assert tree.search(value) is (value in expected)
            assert snapshot(tree.root) == before
        assert_avl(tree, expected)


@pytest.mark.parametrize("reverse", [False, True])
def test_many_sorted_insertions_and_deletions(reverse):
    # Обычный BST превратился бы в цепочку длиной 5000.
    values = sorted(range(5_000), reverse=reverse)
    tree = AVL()
    for value in values:
        tree.insert(value)
    assert_avl(tree, values)
    assert all(tree.search(value) for value in values)
    assert tree.search(-1) is False
    assert tree.search(5_000) is False
    expected = set(values)
    for i, value in enumerate(values):
        tree.delete(value)
        expected.remove(value)
        # Большой тест проверяем порциями; малые выше — после каждого шага.
        if i % 100 == 0:
            assert_avl(tree, expected)
    assert_avl(tree, [])
    assert tree.root is None
