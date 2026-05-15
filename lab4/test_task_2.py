import pytest
from task_2 import sequence_recursive, sequence_iterative


def test_first():
    assert sequence_recursive(1) == 1.0
    assert sequence_iterative(1) == 1.0


def test_second():
    assert sequence_recursive(2) == -1.0 / 8.0
    assert sequence_iterative(2) == -1.0 / 8.0


def test_third():
    # x_3 = (2*(-1/8))/3 + (1*1)/4 = -1/12 + 3/12 = 1/6
    expected = 1.0 / 6.0
    assert sequence_recursive(3) == pytest.approx(expected)
    assert sequence_iterative(3) == pytest.approx(expected)


def test_recursive_and_iterative_match():
    """Проверяем, что обе версии дают одинаковый результат."""
    for n in [1, 2, 3, 5, 10, 15]:
        rec = sequence_recursive(n)
        itr = sequence_iterative(n)
        assert rec == pytest.approx(itr, rel=1e-9)