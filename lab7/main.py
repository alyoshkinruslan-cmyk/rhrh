#!/usr/bin/env python3
"""CLI для лабораторной работы №7 — Пакеты и модули (Typer)."""

import typer
import ast
from typing import Optional

from lab7_package import task4 as t4
from lab7_package import task5 as t5
from lab7_package import task6 as t6

app = typer.Typer(help="Лабораторная работа №7: Пакеты и модули", no_args_is_help=True)


# =================== ЗАДАЧА 4 ===================

@app.command()
def count(lst: str, method: str = "recursive"):
    """Подсчёт числа элементов в списке произвольной глубины."""
    try:
        if lst.startswith('['):
            parsed_list = ast.literal_eval(lst)
        else:
            parsed_list = [int(x) if x.lstrip('-').isdigit() else float(x) for x in lst.split()]
    except Exception as e:
        typer.echo(f"Ошибка парсинга списка: {e}")
        raise typer.Exit(code=1)

    if method == "recursive":
        result = t4.count_recursive(parsed_list)
        typer.echo(f"Количество элементов (рекурсивно): {result}")
    elif method == "iterative":
        result = t4.count_iterative(parsed_list)
        typer.echo(f"Количество элементов (итеративно): {result}")
    else:
        typer.echo("method должен быть 'recursive' или 'iterative'")
        raise typer.Exit(code=1)


@app.command()
def sequence(i: int, method: str = "recursive"):
    """Вычисление i-го члена последовательности."""
    if i < 1:
        typer.echo("i должно быть >= 1")
        raise typer.Exit(code=1)

    if method == "recursive":
        result = t4.sequence_recursive(i)
        typer.echo(f"x_{i} (рекурсивно) = {result}")
    elif method == "iterative":
        result = t4.sequence_iterative(i)
        typer.echo(f"x_{i} (итеративно) = {result}")
    else:
        typer.echo("method должен быть 'recursive' или 'iterative'")
        raise typer.Exit(code=1)


# =================== ЗАДАЧА 5 ===================

@app.command()
def calc(operator: str, initial: float, value: float, times: int = 1):
    """Замыкание-калькулятор с накоплением."""
    try:
        calc_func = t5.make_calc(operator, initial)
        
        if times > 1:
            repeated = t5.repeat(times)(calc_func)
            results = repeated(value)
            typer.echo(f"Результаты ({times} раз): {results}")
        else:
            result = calc_func(value)
            typer.echo(f"Результат: {result}")
    except Exception as e:
        typer.echo(f"Ошибка: {e}")
        raise typer.Exit(code=1)


@app.command()
def fibonacci(n: int, memoized: bool = False):
    """Вычисление n-го числа Фибоначчи (для демонстрации memoize)."""
    if n < 0:
        typer.echo("n должно быть >= 0")
        raise typer.Exit(code=1)

    def fib(n):
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)

    if memoized:
        @t5.memoize(maxsize=128)
        def fib_memo(n):
            if n <= 1:
                return n
            return fib_memo(n - 1) + fib_memo(n - 2)
        
        result = fib_memo(n)
        typer.echo(f"Фибоначчи({n}) с мемоизацией = {result}")
    else:
        result = fib(n)
        typer.echo(f"Фибоначчи({n}) без мемоизации = {result}")


# =================== ЗАДАЧА 6 ===================

@app.command()
def random_gen(
    min_val: int,
    max_val: int,
    count: int = typer.Argument(5, help="Количество чисел"),
    seed: Optional[int] = typer.Option(None, "--seed", "-s", help="Seed для воспроизводимости")
):
    """Генерация случайных чисел через собственный генератор (LCG)."""
    if count < 1:
        typer.echo("count должен быть >= 1")
        raise typer.Exit(code=1)

    try:
        gen = t6.bounded_random(min_val, max_val, seed)
        results = []
        for _ in range(count):
            results.append(next(gen))
        
        typer.echo(f"Сгенерировано {count} чисел в диапазоне [{min_val}, {max_val}]:")
        typer.echo(f"Seed: {seed if seed is not None else 'time-based'}")
        typer.echo(f"Результаты: {results}")
    except Exception as e:
        typer.echo(f"Ошибка: {e}")
        raise typer.Exit(code=1)


@app.command()
def random_batch(
    min_val: int,
    max_val: int,
    count: int = typer.Argument(100000, help="Количество чисел"),
    seed: Optional[int] = typer.Option(None, "--seed", "-s")
):
    """Генерация большого количества чисел с замером времени."""
    try:
        @t6.timer_decorator
        def generate():
            gen = t6.bounded_random(min_val, max_val, seed)
            return [next(gen) for _ in range(count)]
        
        results = generate()
        typer.echo(f"Сгенерировано {count} чисел")
        typer.echo(f"Первые 10: {results[:10]}")
        typer.echo(f"Последние 10: {results[-10:]}")
    except Exception as e:
        typer.echo(f"Ошибка: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()