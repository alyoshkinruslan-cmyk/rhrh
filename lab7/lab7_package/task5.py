"""Модуль из лабораторной работы №5: замыкания и декораторы."""

import time
from functools import wraps


def make_calc(operator, initial):
    """Создать замыкание-калькулятор с накоплением."""
    result = initial
    
    def calc(value):
        nonlocal result
        if operator == '+':
            result += value
        elif operator == '-':
            result -= value
        elif operator == '*':
            result *= value
        elif operator == '/':
            if value == 0:
                raise ValueError("Деление на ноль")
            result /= value
        else:
            raise ValueError(f"Неизвестный оператор: {operator}")
        return result
    
    return calc


def repeat(times):
    """Декоратор многократного запуска функции."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator


def memoize(maxsize=None):
    """Декоратор мемоизации с опциональным ограничением кэша."""
    def decorator(func):
        cache = {}
        order = []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in cache:
                return cache[key]
            
            result = func(*args, **kwargs)
            cache[key] = result
            order.append(key)
            
            if maxsize is not None and len(cache) > maxsize:
                oldest = order.pop(0)
                if oldest in cache:
                    del cache[oldest]
            
            return result
        return wrapper
    return decorator


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