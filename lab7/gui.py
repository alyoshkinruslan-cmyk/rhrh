"""GUI приложение для лабораторной работы №7 (Medium)."""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import ast

from lab7_package import task4 as t4
from lab7_package import task5 as t5
from lab7_package import task6 as t6


class Lab7GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab7 GUI — Пакеты и модули")
        self.root.geometry("700x500")

        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self._build_count_tab(notebook)
        self._build_sequence_tab(notebook)
        self._build_calc_tab(notebook)
        self._build_random_tab(notebook)

    def _build_count_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Подсчёт элементов")

        ttk.Label(frame, text="Введите список (например: [1, [2, 3], [4, 5]] или 1 2 3 4):").pack(pady=5)
        self.count_entry = ttk.Entry(frame, width=60)
        self.count_entry.pack(pady=5)
        self.count_entry.insert(0, "[1, [2, 3], [4, 5]]")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Рекурсивно", command=lambda: self._calc_count("recursive")).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Итеративно", command=lambda: self._calc_count("iterative")).pack(side='left', padx=5)

        self.count_result = ttk.Label(frame, text="Результат: ", font=('Arial', 12))
        self.count_result.pack(pady=10)

    def _calc_count(self, method):
        lst_str = self.count_entry.get().strip()
        try:
            if lst_str.startswith('['):
                parsed = ast.literal_eval(lst_str)
            else:
                parsed = [int(x) if x.lstrip('-').isdigit() else float(x) for x in lst_str.split()]

            if method == "recursive":
                result = t4.count_recursive(parsed)
            else:
                result = t4.count_iterative(parsed)

            self.count_result.config(text=f"Количество элементов ({method}): {result}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неверный ввод: {e}")

    def _build_sequence_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Последовательность")

        ttk.Label(frame, text="Введите i (номер члена, >= 1):").pack(pady=5)
        self.seq_entry = ttk.Entry(frame, width=20)
        self.seq_entry.pack(pady=5)
        self.seq_entry.insert(0, "5")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Рекурсивно", command=lambda: self._calc_seq("recursive")).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Итеративно", command=lambda: self._calc_seq("iterative")).pack(side='left', padx=5)

        self.seq_result = ttk.Label(frame, text="Результат: ", font=('Arial', 12))
        self.seq_result.pack(pady=10)

    def _calc_seq(self, method):
        try:
            i = int(self.seq_entry.get())
            if i < 1:
                raise ValueError("i должно быть >= 1")

            if method == "recursive":
                result = t4.sequence_recursive(i)
            else:
                result = t4.sequence_iterative(i)

            self.seq_result.config(text=f"x_{i} ({method}) = {result:.10f}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _build_calc_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Калькулятор")

        ttk.Label(frame, text="Оператор (+, -, *, /):").pack(pady=5)
        self.calc_op = ttk.Entry(frame, width=10)
        self.calc_op.pack(pady=5)
        self.calc_op.insert(0, "+")

        ttk.Label(frame, text="Начальное значение:").pack(pady=5)
        self.calc_initial = ttk.Entry(frame, width=15)
        self.calc_initial.pack(pady=5)
        self.calc_initial.insert(0, "0")

        ttk.Label(frame, text="Значение для операции:").pack(pady=5)
        self.calc_value = ttk.Entry(frame, width=15)
        self.calc_value.pack(pady=5)
        self.calc_value.insert(0, "10")

        ttk.Label(frame, text="Количество повторов:").pack(pady=5)
        self.calc_times = ttk.Spinbox(frame, from_=1, to=10, width=10)
        self.calc_times.set(1)
        self.calc_times.pack(pady=5)

        ttk.Button(frame, text="Вычислить", command=self._do_calc).pack(pady=5)

        self.calc_result = scrolledtext.ScrolledText(frame, width=60, height=5, wrap=tk.WORD)
        self.calc_result.pack(pady=10, fill='both', expand=True)
        self.calc_result.insert('1.0', "Результат появится здесь...")
        self.calc_result.config(state='disabled')

    def _do_calc(self):
        try:
            op = self.calc_op.get().strip()
            initial = float(self.calc_initial.get())
            value = float(self.calc_value.get())
            times = int(self.calc_times.get())

            calc_func = t5.make_calc(op, initial)

            if times > 1:
                repeated = t5.repeat(times)(calc_func)
                results = repeated(value)
                text = f"Оператор: {op}, начальное: {initial}\n"
                text += f"Применено {times} раз с значением {value}:\n"
                text += str(results)
            else:
                result = calc_func(value)
                text = f"Оператор: {op}, начальное: {initial}\n"
                text += f"Результат: {result}"

            self.calc_result.config(state='normal')
            self.calc_result.delete('1.0', tk.END)
            self.calc_result.insert('1.0', text)
            self.calc_result.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _build_random_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Генератор")

        ttk.Label(frame, text="Минимум:").pack(pady=5)
        self.rand_min = ttk.Entry(frame, width=15)
        self.rand_min.pack(pady=5)
        self.rand_min.insert(0, "1")

        ttk.Label(frame, text="Максимум:").pack(pady=5)
        self.rand_max = ttk.Entry(frame, width=15)
        self.rand_max.pack(pady=5)
        self.rand_max.insert(0, "100")

        ttk.Label(frame, text="Количество:").pack(pady=5)
        self.rand_count = ttk.Spinbox(frame, from_=1, to=1000, width=10)
        self.rand_count.set(10)
        self.rand_count.pack(pady=5)

        ttk.Label(frame, text="Seed (опционально):").pack(pady=5)
        self.rand_seed = ttk.Entry(frame, width=15)
        self.rand_seed.pack(pady=5)
        self.rand_seed.insert(0, "42")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Сгенерировать", command=self._generate_random).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Со случайным seed", command=self._generate_random_no_seed).pack(side='left', padx=5)

        self.rand_result = scrolledtext.ScrolledText(frame, width=70, height=10, wrap=tk.WORD)
        self.rand_result.pack(pady=10, fill='both', expand=True)
        self.rand_result.insert('1.0', "Числа появятся здесь...")
        self.rand_result.config(state='disabled')

    def _insert_rand(self, text):
        self.rand_result.config(state='normal')
        self.rand_result.delete('1.0', tk.END)
        self.rand_result.insert('1.0', text)
        self.rand_result.config(state='disabled')

    def _generate_random(self):
        try:
            min_val = int(self.rand_min.get())
            max_val = int(self.rand_max.get())
            count = int(self.rand_count.get())
            seed_str = self.rand_seed.get().strip()
            seed = int(seed_str) if seed_str else None

            gen = t6.bounded_random(min_val, max_val, seed)
            results = [next(gen) for _ in range(count)]

            text = f"Диапазон: [{min_val}, {max_val}]\n"
            text += f"Seed: {seed if seed is not None else 'time-based'}\n"
            text += f"Результаты ({count} шт.):\n{results}"
            self._insert_rand(text)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _generate_random_no_seed(self):
        self.rand_seed.delete(0, tk.END)
        self._generate_random()


def main():
    root = tk.Tk()
    app = Lab7GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()