import pytest
from task_1 import count_recursive, count_iterative


def test_empty_list():
    assert count_recursive([]) == 0
    assert count_iterative([]) == 0


def test_flat_list():
    assert count_recursive([1, 2, 3]) == 3
    assert count_iterative([1, 2, 3]) == 3


def test_nested_one_level():
    assert count_recursive(["x", "y", ["z"]]) == 4
    assert count_iterative(["x", "y", ["z"]]) == 4


def test_deep_nested():
    assert count_recursive([1, 2, [3, 4, [5]]]) == 7
    assert count_iterative([1, 2, [3, 4, [5]]]) == 7


def test_mixed_types():
    assert count_recursive([1, "a", [2.5, [None, True]]]) == 7
    assert count_iterative([1, "a", [2.5, [None, True]]]) == 7


def test_empty_nested():
    assert count_recursive([[], [1, []], 2]) == 5
    assert count_iterative([[], [1, []], 2]) == 5