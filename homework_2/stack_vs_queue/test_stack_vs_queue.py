import pytest

from stack_vs_queue import Queue, Stack


def test_new_structures_are_empty():
    stack = Stack()
    queue = Queue()

    assert stack.is_empty()
    assert queue.is_empty()
    assert len(stack) == 0
    assert len(queue) == 0


def test_stack_uses_lifo_order():
    stack = Stack()

    for value in (10, 20, 30):
        stack.push(value)

    assert stack.peek() == 30
    assert len(stack) == 3
    assert [stack.pop(), stack.pop(), stack.pop()] == [30, 20, 10]
    assert stack.is_empty()


def test_queue_uses_fifo_order():
    queue = Queue()

    for value in (10, 20, 30):
        queue.enqueue(value)

    assert queue.peek() == 10
    assert len(queue) == 3
    assert [queue.dequeue(), queue.dequeue(), queue.dequeue()] == [10, 20, 30]
    assert queue.is_empty()


def test_peek_does_not_remove_an_element():
    stack = Stack()
    queue = Queue()
    stack.push("value")
    queue.enqueue("value")

    assert stack.peek() == "value"
    assert stack.peek() == "value"
    assert len(stack) == 1

    assert queue.peek() == "value"
    assert queue.peek() == "value"
    assert len(queue) == 1


def test_queue_works_after_becoming_empty():
    queue = Queue()
    queue.enqueue(1)
    assert queue.dequeue() == 1

    queue.enqueue(2)

    assert queue.peek() == 2
    assert queue.dequeue() == 2
    assert queue.is_empty()


def test_structures_can_store_none():
    stack = Stack()
    queue = Queue()

    stack.push(None)
    queue.enqueue(None)

    assert stack.pop() is None
    assert queue.dequeue() is None


@pytest.mark.parametrize("structure", [Stack, Queue])
def test_peek_from_empty_structure_raises_index_error(structure):
    with pytest.raises(IndexError):
        structure().peek()


def test_pop_from_empty_stack_raises_index_error():
    with pytest.raises(IndexError):
        Stack().pop()


def test_dequeue_from_empty_queue_raises_index_error():
    with pytest.raises(IndexError):
        Queue().dequeue()
