"""
Lab 5: Замыкания и декораторы в Python
Вариант 1
"""

from functools import wraps


# ==================== Замыкание-калькулятор ====================

def make_calc(operator, initial=0):
    """
    Создает замыкание-калькулятор.
    
    Args:
        operator: одна из '+', '-', '*', '/'
        initial: начальное значение аккумулятора
    
    Returns:
        Функцию calc(value), которая применяет операцию и возвращает накопленный результат.
    """
    if operator not in ('+', '-', '*', '/'):
        raise ValueError(f"Неподдерживаемая операция: {operator}")
    
    result = initial
    
    def calc(value):
        nonlocal result
        if operator == '+':
            result = result + value
        elif operator == '-':
            result = result - value
        elif operator == '*':
            result = result * value
        elif operator == '/':
            if value == 0:
                raise ZeroDivisionError("Деление на ноль")
            result = result / value
        return result
    
    return calc


# ==================== Декоратор многократного запуска ====================

def repeat(times=1):
    """
    Декоратор, запускающий функцию `times` раз с одними и теми же аргументами.
    Возвращает список результатов.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(times)]
        return wrapper
    return decorator


# ==================== MEDIUM: Декоратор с опциональным параметром ====================

def memoize(maxsize=None):
    """
    Декоратор мемоизации с опциональным ограничением кэша.
    Корректно работает с рекурсивными функциями.
    
    Использование:
        @memoize
        def fib(n): ...
        
        @memoize(maxsize=128)
        def fib(n): ...
    """
    def decorator(func):
        cache = {}
        order = []  # для отслеживания порядка (простая LRU при maxsize)
        
        @wraps(func)
        def wrapper(*args):
            if args in cache:
                return cache[args]
            
            result = func(*args)
            cache[args] = result
            
            if maxsize is not None:
                order.append(args)
                if len(order) > maxsize:
                    oldest = order.pop(0)
                    del cache[oldest]
            
            return result
        
        wrapper.cache = cache
        wrapper.cache_info = lambda: f"Cache size: {len(cache)}, maxsize: {maxsize}"
        return wrapper
    
    # Если декоратор применен без скобок: @memoize
    if callable(maxsize):
        func = maxsize
        maxsize = None
        return decorator(func)
    
    return decorator


# ==================== ДЕМОНСТРАЦИЯ ====================

if __name__ == "__main__":
    print("=" * 50)
    print("RARE: Замыкание-калькулятор")
    print("=" * 50)
    
    # Пример из задания: умножение, initial=1
    calc = make_calc("*", initial=1)
    print(f"calc(5) = {calc(5)}")   # 1 * 5 = 5
    print(f"calc(2) = {calc(2)}")   # 5 * 2 = 10
    print(f"calc(3) = {calc(3)}")   # 10 * 3 = 30
    
    # Другие операции
    calc_plus = make_calc("+", initial=10)
    print(f"calc_plus(5) = {calc_plus(5)}")   # 15
    print(f"calc_plus(3) = {calc_plus(3)}")   # 18
    
    print("\n" + "=" * 50)
    print("RARE: Декоратор repeat() применен к замыканию")
    print("=" * 50)
    
    # Применяем декоратор к замыканию вручную (динамически создано)
    repeated_calc = repeat(3)(calc)
    print("repeat(3)(calc)(2):")
    results = repeated_calc(2)
    print(f"Результаты: {results}")
    print("(Каждый вызов накапливает состояние: 30*2=60, 60*2=120, 120*2=240)")
    
    print("\n" + "=" * 50)
    print("MEDIUM: Декоратор memoize() и рекурсия")
    print("=" * 50)
    
    @memoize
    def fibonacci(n):
        """Рекурсивное вычисление чисел Фибоначчи."""
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    
    print(f"fibonacci(10) = {fibonacci(10)}")
    print(f"fibonacci(20) = {fibonacci(20)}")
    print(fibonacci.cache_info())
    print(f"Кэш содержит {len(fibonacci.cache)} записей")
    
    # Демонстрация с ограничением кэша
    @memoize(maxsize=5)
    def fib_limited(n):
        if n < 2:
            return n
        return fib_limited(n - 1) + fib_limited(n - 2)
    
    print(f"\nfib_limited(8) = {fib_limited(8)}")
    print(fib_limited.cache_info())