"""Модуль из лабораторной работы №4: рекурсия."""


def count_recursive(lst):
    """Рекурсивный подсчёт числа элементов в списке произвольной глубины."""
    count = 0
    for item in lst:
        if isinstance(item, list):
            count += count_recursive(item)
        else:
            count += 1
    return count


def count_iterative(lst):
    """Итеративный подсчёт числа элементов через стек."""
    stack = list(lst)
    count = 0
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(item)
        else:
            count += 1
    return count


def sequence_recursive(i):
    """Рекурсивное вычисление i-го члена последовательности.
    
    Формула: x_i = ((i-1)*x_{i-1})/3 + ((i-2)*x_{i-2})/4
    Начальные условия: x_1 = 1, x_2 = -1/8
    """
    if i == 1:
        return 1.0
    if i == 2:
        return -1.0 / 8.0
    
    x_prev1 = sequence_recursive(i - 1)
    x_prev2 = sequence_recursive(i - 2)
    
    x_i = ((i - 1) * x_prev1) / 3.0 + ((i - 2) * x_prev2) / 4.0
    return x_i


def sequence_iterative(i):
    """Итеративное вычисление i-го члена последовательности."""
    if i == 1:
        return 1.0
    if i == 2:
        return -1.0 / 8.0
    
    x_prev2 = 1.0
    x_prev1 = -1.0 / 8.0
    
    for n in range(3, i + 1):
        x_current = ((n - 1) * x_prev1) / 3.0 + ((n - 2) * x_prev2) / 4.0
        x_prev2 = x_prev1
        x_prev1 = x_current
    
    return x_prev1