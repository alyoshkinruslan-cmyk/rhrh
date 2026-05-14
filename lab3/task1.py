"""
Тимофей составляет 5-буквенные коды из букв Т, И, М, О, Ф, Е, Й.
Буква Й может использоваться не более 1 раза, не на 1-м/последнем месте,
не рядом с буквой И. Остальные буквы могут повторяться произвольно.
Сколько различных кодов может составить Тимофей?

Решение через itertools.product с фильтрацией.
"""

import itertools


def count_codes() -> int:
    """
    Подсчитывает количество допустимых 5-буквенных кодов.

    >>> count_codes()
    10476
    """
    letters = ['Т', 'И', 'М', 'О', 'Ф', 'Е', 'Й']
    count = 0

    for word in itertools.product(letters, repeat=5):
        word_str = ''.join(word)
        y_count = word_str.count('Й')

        # Й не более 1 раза
        if y_count > 1:
            continue

        # Если Й присутствует — проверяем ограничения
        if y_count == 1:
            y_pos = word_str.index('Й')

            # Не на первом месте (индекс 0)
            if y_pos == 0:
                continue

            # Не на последнем месте (индекс 4)
            if y_pos == 4:
                continue

            # Не рядом с И (слева или справа)
            if word_str[y_pos - 1] == 'И':
                continue
            if y_pos < 4 and word_str[y_pos + 1] == 'И':
                continue

        count += 1

    return count


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

    result = count_codes()
    print(f"\nОтвет: {result} различных кодов")