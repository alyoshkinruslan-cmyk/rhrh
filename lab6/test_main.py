"""
Тесты для генератора случайных чисел (Medium)
Запуск: pytest test_main.py -v
"""

import pytest
from main import bounded_random, lcg_random


class TestBoundedRandom:
    def test_values_in_range(self):
        """Все значения лежат в заданном диапазоне."""
        gen = bounded_random(10, 20, seed=42)
        for _ in range(1000):
            val = next(gen)
            assert 10 <= val <= 20

    def test_determinism(self):
        """Одинаковый seed → одинаковая последовательность."""
        gen1 = bounded_random(1, 100, seed=12345)
        gen2 = bounded_random(1, 100, seed=12345)
        for _ in range(100):
            assert next(gen1) == next(gen2)

    def test_single_value_range(self):
        """Диапазон из одного числа всегда возвращает его."""
        gen = bounded_random(5, 5, seed=99)
        for _ in range(50):
            assert next(gen) == 5

    def test_invalid_range(self):
        """min_val > max_val вызывает ValueError."""
        with pytest.raises(ValueError):
            bounded_random(100, 1)

    def test_non_integer_bounds(self):
        """Нецелочисленные границы вызывают TypeError."""
        with pytest.raises(TypeError):
            bounded_random(1.5, 10)

    def test_negative_range(self):
        """Корректная работа с отрицательными числами."""
        gen = bounded_random(-50, -10, seed=7)
        for _ in range(100):
            val = next(gen)
            assert -50 <= val <= -10


class TestLcgRandom:
    def test_infinite_generation(self):
        """Генератор работает бесконечно."""
        gen = lcg_random(seed=1)
        values = [next(gen) for _ in range(10000)]
        assert len(values) == 10000
        assert len(set(values[:100])) > 1  # не константа

    def test_different_seeds(self):
        """Разные seed дают разные последовательности."""
        gen1 = lcg_random(seed=1)
        gen2 = lcg_random(seed=2)
        vals1 = [next(gen1) for _ in range(10)]
        vals2 = [next(gen2) for _ in range(10)]
        assert vals1 != vals2