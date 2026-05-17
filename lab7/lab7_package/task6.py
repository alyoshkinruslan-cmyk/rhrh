"""Модуль из лабораторной работы №6: генераторы."""

import time
from functools import wraps


def timer_decorator(func):
    """Декоратор для замера времени выполнения функции."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[ДЕКОРАТОР] Время выполнения: {end - start:.6f} сек.")
        return result
    return wrapper


def bounded_random(min_val, max_val, seed=None):
    """Генератор случайных чисел (линейный конгруэнтный метод).
    
    Не использует модуль random.
    """
    if not isinstance(min_val, int) or not isinstance(max_val, int):
        raise TypeError("Границы диапазона должны быть целыми числами")
    if min_val > max_val:
        raise ValueError("min_val не может быть больше max_val")
    
    a = 1103515245
    c = 12345
    m = 2**31
    
    if seed is None:
        state = int(time.time() * 1000) % m
    else:
        if not isinstance(seed, int):
            raise TypeError("seed должен быть целым числом")
        state = seed % m
    
    while True:
        state = (a * state + c) % m
        yield min_val + (state % (max_val - min_val + 1))