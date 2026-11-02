import inspect

import pytest

from tracer.trace_calls import tracer


def test_factorial_trace(capsys):
    @tracer
    def factorial(n):
        return 1 if n == 0 else n * factorial(n - 1)

    assert factorial(3) == 6
    assert capsys.readouterr().out.splitlines() == [
        "-> factorial(3)",
        "  -> factorial(2)",
        "    -> factorial(1)",
        "      -> factorial(0)",
        "      <- factorial = 1",
        "    <- factorial = 1",
        "  <- factorial = 2",
        "<- factorial = 6",
    ]
    assert factorial(0) == 1
    assert capsys.readouterr().out == "-> factorial(0)\n<- factorial = 1\n"


def test_branching_recursion_from_visualization(capsys):
    @tracer
    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    assert fib(3) == 2
    assert capsys.readouterr().out.splitlines() == [
        "-> fib(3)",
        "  -> fib(2)",
        "    -> fib(1)",
        "    <- fib = 1",
        "    -> fib(0)",
        "    <- fib = 0",
        "  <- fib = 1",
        "  -> fib(1)",
        "  <- fib = 1",
        "<- fib = 2",
    ]


def test_arguments_and_metadata(capsys):
    def join(first, *parts, separator=":", **options):
        """Соединяет строки с суффиксом."""
        return separator.join((first,) + parts) + options.get("suffix", "")

    wrapped = tracer(join)
    assert wrapped("a", "b", separator="/", suffix="!") == "a/b!"
    assert capsys.readouterr().out.splitlines() == [
        "-> join('a', 'b', separator='/', suffix='!')",
        "<- join = 'a/b!'",
    ]
    assert wrapped.__name__ == join.__name__
    assert wrapped.__doc__ == join.__doc__
    assert wrapped.__wrapped__ is join
    assert inspect.signature(wrapped) == inspect.signature(join)


@pytest.mark.parametrize("value", [None, 0, False, [], {"x": [1, 2]}])
def test_result_is_not_copied(value, capsys):
    @tracer
    def get_value():
        return value

    assert get_value() is value
    assert capsys.readouterr().out.splitlines() == [
        "-> get_value()", f"<- get_value = {value!r}",
    ]


def test_mutual_recursion_uses_one_stack(capsys):
    @tracer
    def even(n):
        return True if n == 0 else odd(n - 1)

    @tracer
    def odd(n):
        return False if n == 0 else even(n - 1)

    assert even(2) is True
    assert capsys.readouterr().out.splitlines() == [
        "-> even(2)",
        "  -> odd(1)",
        "    -> even(0)",
        "    <- even = True",
        "  <- odd = True",
        "<- even = True",
    ]


def test_exception_propagates_and_depth_is_restored(capsys):
    error = ValueError("boom")

    @tracer
    def fail(n):
        if n == 0:
            raise error
        return fail(n - 1)

    for _ in range(2):
        with pytest.raises(ValueError) as caught:
            fail(1)
        assert caught.value is error
        assert capsys.readouterr().out.splitlines() == [
            "-> fail(1)",
            "  -> fail(0)",
            "  !! fail: ValueError('boom')",
            "!! fail: ValueError('boom')",
        ]

    @tracer
    def ok():
        return 42

    assert ok() == 42
    assert capsys.readouterr().out == "-> ok()\n<- ok = 42\n"


def test_exception_caught_inside_parent(capsys):
    @tracer
    def child(fail):
        if fail:
            raise ValueError("boom")
        return 7

    @tracer
    def parent():
        try:
            child(True)
        except ValueError:
            return child(False)

    assert parent() == 7
    assert capsys.readouterr().out.splitlines() == [
        "-> parent()",
        "  -> child(True)",
        "  !! child: ValueError('boom')",
        "  -> child(False)",
        "  <- child = 7",
        "<- parent = 7",
    ]
