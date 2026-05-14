"""
Найдите среди целых чисел, принадлежащих отрезку [174457; 174505],
числа, имеющие ровно два различных натуральных делителя,
не считая единицы и самого числа.
Для каждого найденного числа выведите эти два делителя
в порядке возрастания (по одной паре на строку).
"""

def find_special_numbers() -> list[tuple[int, int, int]]:
    """
    Находит числа с ровно двумя делителями (кроме 1 и себя).
    Возвращает список кортежей: (число, делитель_1, делитель_2).

    >>> data = find_special_numbers()
    >>> len(data) > 0
    True
    >>> all(len(str(t[0])) > 0 for t in data)
    True
    """
    results: list[tuple[int, int, int]] = []

    for n in range(174457, 174506):  # включительно 174505
        divisors: list[int] = []

        # Ищем делители от 2 до sqrt(n)
        for d in range(2, int(n**0.5) + 1):
            if n % d == 0:
                divisors.append(d)
                other = n // d
                if other != d:
                    divisors.append(other)

        # Убираем дубликаты, сортируем
        divisors = sorted(set(divisors))

        # Ровно 2 делителя (не считая 1 и самого числа)
        if len(divisors) == 2:
            results.append((n, divisors[0], divisors[1]))

    return results


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

    results = find_special_numbers()
    print(f"\nНайдено чисел: {len(results)}\n")
    print("Делители (в порядке возрастания числа):")
    for n, d1, d2 in results:
        print(f"{d1} {d2}")