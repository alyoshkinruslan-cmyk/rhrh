# Формула: x_i = ((i-1)*x_{i-1})/3 + ((i-2)*x_{i-2})/4
# Начальные условия: x_1 = 1, x_2 = -1/8

def sequence_recursive(i):
    """Рекурсивный расчёт i-го члена последовательности."""
    if i == 1:
        return 1.0
    if i == 2:
        return -1.0 / 8.0
    return ((i - 1) * sequence_recursive(i - 1)) / 3 + ((i - 2) * sequence_recursive(i - 2)) / 4


def sequence_iterative(i):
    """Итеративный расчёт i-го члена. Хранит только 2 предыдущих значения."""
    if i == 1:
        return 1.0
    if i == 2:
        return -1.0 / 8.0

    x_prev2 = 1.0          # x_{i-2} при i=3 это x_1
    x_prev1 = -1.0 / 8.0   # x_{i-1} при i=3 это x_2

    for n in range(3, i + 1):
        x_current = ((n - 1) * x_prev1) / 3 + ((n - 2) * x_prev2) / 4
        x_prev2 = x_prev1
        x_prev1 = x_current

    return x_prev1


# Пример использования
if __name__ == "__main__":
    for n in [1, 2, 3, 5, 10]:
        rec = sequence_recursive(n)
        itr = sequence_iterative(n)
        print(f"n={n}: recursive={rec}, iterative={itr}")