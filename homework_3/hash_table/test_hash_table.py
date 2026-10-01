import pytest

from hash_table import HashTable


class CollisionKey:
    # Разные ключи специально получают одинаковый хеш.
    def __init__(self, value):
        self.value = value

    def __hash__(self):
        return 5

    def __eq__(self, other):
        return isinstance(other, CollisionKey) and self.value == other.value


def test_empty_table():
    table = HashTable()
    assert len(table) == 0
    assert len(table.buckets) == 8
    assert "missing" not in table


@pytest.mark.parametrize("method", ["get", "delete"])
def test_missing_key(method):
    table = HashTable()
    table.put("present", 10)
    with pytest.raises(KeyError) as error:
        getattr(table, method)("missing")
    assert error.value.args == ("missing",)
    assert len(table) == 1
    assert table.get("present") == 10


@pytest.mark.parametrize("key", ["кот", "", 0, -100, 10**30, ("a", 2), None])
def test_different_key_types(key):
    table = HashTable()
    table.put(key, "value")
    assert table.get(key) == "value"
    assert key in table
    table.delete(key)
    assert key not in table
    assert len(table) == 0


def test_update_and_none_value():
    table = HashTable()
    table.put("key", 10)
    table.put("key", None)
    assert len(table) == 1
    assert table.get("key") is None
    assert "key" in table


def test_values_are_not_copied():
    table = HashTable()
    value = [1, 2]
    table.put("key", value)
    value.append(3)
    assert table.get("key") is value
    assert table.get("key") == [1, 2, 3]


def test_equal_keys_update_one_entry():
    table = HashTable()
    table.put(1, "first")
    table.put(True, "second")
    assert len(table) == 1
    assert table.get(1) == "second"


def test_same_nan_object_as_key():
    table = HashTable()
    key = float("nan")
    table.put(key, 10)
    table.put(key, 20)
    assert len(table) == 1
    assert table.get(key) == 20
    table.delete(key)
    assert key not in table


@pytest.mark.parametrize("removed", [0, 1, 2])
def test_delete_from_collision_chain(removed):
    table = HashTable()
    for i in range(3):
        table.put(CollisionKey(i), i * 10)
    table.delete(CollisionKey(removed))
    assert len(table) == 2
    assert CollisionKey(removed) not in table
    for i in range(3):
        if i != removed:
            assert table.get(CollisionKey(i)) == i * 10
    with pytest.raises(KeyError):
        table.delete(CollisionKey(removed))
    table.put(CollisionKey(removed), 99)
    assert len(table) == 3
    assert table.get(CollisionKey(removed)) == 99


def test_collisions_survive_multiple_resizes():
    table = HashTable(capacity=1)
    for i in range(100):
        table.put(CollisionKey(i), i)
    table.put(CollisionKey(50), -1)
    assert len(table) == 100
    for i in range(100):
        assert table.get(CollisionKey(i)) == (-1 if i == 50 else i)
    assert CollisionKey(100) not in table


@pytest.mark.parametrize("capacity, trigger", [(1, 1), (3, 2), (8, 6)])
def test_resize_at_two_thirds(capacity, trigger):
    table = HashTable(capacity)
    for i in range(trigger - 1):
        table.put(i, i)
    assert len(table.buckets) == capacity
    if trigger > 1:
        table.put(0, "updated")
        assert len(table) == trigger - 1
        assert len(table.buckets) == capacity
    table.put(trigger - 1, "last")
    assert len(table.buckets) == capacity * 2
    assert len(table) == trigger
    assert table.get(trigger - 1) == "last"
    if trigger > 1:
        assert table.get(0) == "updated"


def test_rehash_changes_bucket_index():
    table = HashTable(3)
    table.put(1, "A")
    table.put(4, "B")
    assert len(table.buckets) == 6
    assert table.buckets[1] == [[1, "A"]]
    assert table.buckets[4] == [[4, "B"]]
    assert table.get(1) == "A"
    assert table.get(4) == "B"


def test_many_insertions_deletions_and_reuse():
    table = HashTable()
    for i in range(5_000):
        table.put(i, -i)
    assert len(table) == 5_000
    for i in range(5_000):
        assert table.get(i) == -i
    capacity = len(table.buckets)
    for i in range(5_000):
        table.delete(i)
    assert len(table) == 0
    assert all(bucket == [] for bucket in table.buckets)
    assert len(table.buckets) == capacity
    table.put("new", 123)
    assert table.get("new") == 123
    assert len(table) == 1


@pytest.mark.parametrize("capacity", [0, -1])
def test_nonpositive_capacity(capacity):
    with pytest.raises(ValueError):
        HashTable(capacity)


@pytest.mark.parametrize("capacity", [1.5, "8", None, True])
def test_noninteger_capacity(capacity):
    with pytest.raises(TypeError):
        HashTable(capacity)


@pytest.mark.parametrize("method", ["put", "get", "delete", "__contains__"])
def test_unhashable_key(method):
    table = HashTable()
    with pytest.raises(TypeError):
        if method == "put":
            table.put([], 10)
        else:
            getattr(table, method)([])
    assert len(table) == 0


def test_storage_uses_lists_and_independent_buckets():
    table = HashTable()
    table.put(0, "A")
    assert table.buckets[1] == []
    assert type(table.buckets) is list
    for bucket in table.buckets:
        assert type(bucket) is list
        for pair in bucket:
            assert type(pair) is list
            assert len(pair) == 2
