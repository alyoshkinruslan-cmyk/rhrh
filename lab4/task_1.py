
def count_recursive(lst):
    """Рекурсивно считает все элементы, включая вложенные списки.
    Сам список тоже учитывается как элемент (+1), плюс его содержимое."""
    total = 0
    for item in lst:
        total += 1                      # сам элемент
        if isinstance(item, list):
            total += count_recursive(item)  # плюс всё внутри него
    return total


def count_iterative(lst):
    """Итеративная версия через стек. Без рекурсии."""
    stack = list(lst)
    total = 0
    while stack:
        item = stack.pop()
        total += 1                      # считаем сам элемент
        if isinstance(item, list):
            stack.extend(item)          # раскрываем список в стек
    return total


# Пример использования
if __name__ == "__main__":
    print(count_recursive([]))                    # 0
    print(count_recursive([1, 2, 3]))             # 3
    print(count_recursive(["x", "y", ["z"]]))     # 4
    print(count_recursive([1, 2, [3, 4, [5]]]))   # 7

    print(count_iterative([]))                    # 0
    print(count_iterative([1, 2, 3]))             # 3
    print(count_iterative(["x", "y", ["z"]]))     # 4
    print(count_iterative([1, 2, [3, 4, [5]]]))   # 7