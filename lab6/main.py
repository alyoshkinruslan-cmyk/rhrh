"""
Lab 6: Генераторы в Python
Вариант 1 (Rare + Medium)
"""

import time
from functools import wraps


# ==================== Декоратор для замера времени ====================

def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[ДЕКОРАТОР] Время выполнения: {end - start:.4f} сек.")
        return result
    return wrapper


# ==================== RARE: Генератор случайных чисел ====================

def lcg_random(seed=None):
    """
    Линейный конгруэнтный генератор (LCG).
    Параметры из Numerical Recipes.
    """
    if seed is None:
        seed = int(time.time() * 1000) % (2**32)
    
    x = seed
    while True:
        x = (1664525 * x + 1013904223) % (2**32)
        yield x


def bounded_random(min_val, max_val, seed=None):
    """
    Генератор случайных целых чисел в диапазоне [min_val, max_val].
    Не использует готовые реализации ГПСЧ (модуль random).
    """
    if not isinstance(min_val, int) or not isinstance(max_val, int):
        raise TypeError("Границы диапазона должны быть целыми числами")
    
    if min_val > max_val:
        raise ValueError("min_val не может быть больше max_val")
    
    range_size = max_val - min_val + 1
    gen = lcg_random(seed)
    
    def _generator():
        while True:
            raw = next(gen)
            yield min_val + (raw % range_size)
    
    return _generator()


# ==================== ДЕМОНСТРАЦИЯ ====================

if __name__ == "__main__":
    print("=" * 60)
    print("ЛАБОРАТОРНАЯ РАБОТА №6: Генераторы")
    print("=" * 60)
    
    # 1. Генерация чисел в диапазоне
    print("\n[ИНФО] 10 чисел в диапазоне [1, 100] (seed=42):")
    gen = bounded_random(1, 100, seed=42)
    numbers = [next(gen) for _ in range(10)]
    print(numbers)
    
    # 2. Проверка детерминизма
    print("\n[ИНФО] Проверка детерминизма (seed=123):")
    gen1 = bounded_random(0, 10, seed=123)
    gen2 = bounded_random(0, 10, seed=123)
    seq1 = [next(gen1) for _ in range(5)]
    seq2 = [next(gen2) for _ in range(5)]
    print(f"Последовательность 1: {seq1}")
    print(f"Последовательность 2: {seq2}")
    print(f"Совпадают: {seq1 == seq2}")
    
    # 3. Декоратор на batch-генерации
    @timer_decorator
    def generate_batch():
        g = bounded_random(1, 1000, seed=999)
        return [next(g) for _ in range(10000)]
    
    print("\n[ИНФО] Генерация 10 000 чисел с замером времени:")
    batch = generate_batch()
    print(f"Первые 5: {batch[:5]}")
    print(f"Последние 5: {batch[-5:]}")
    
    # 4. Граничный случай
    print("\n[ИНФО] Граничный случай [7, 7]:")
    const_gen = bounded_random(7, 7, seed=1)
    print([next(const_gen) for _ in range(5)])
    
    print("\n[ИНФО] Работа программы завершена")