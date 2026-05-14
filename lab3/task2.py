"""
Сколько единиц содержится в двоичной записи значения выражения:
4^2020 + 2^2017 - 15
"""

def count_ones_in_binary() -> int:
    """
    Возвращает количество единиц в двоичной записи числа.

    >>> count_ones_in_binary()
    2015
    """
    value = 4**2020 + 2**2017 - 15
    return bin(value).count('1')


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

    result = count_ones_in_binary()
    print(f"\nКоличество единиц в двоичной записи: {result}")