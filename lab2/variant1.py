import numpy as np
import matplotlib.pyplot as plt

# === Функция варианта 1 ===
def f1(x):
    return np.cos(x + x**3)

def f2(x):
    return np.exp(-x**2) - x**2 + 2*x

# Данные для графика
x1 = np.linspace(0, 1, 300)
x2 = np.linspace(1, 2, 300)
y1 = f1(x1)
y2 = f2(x2)

# === Касательная в точке x0 = 0.5 ===
x0 = 0.5
y0 = f1(x0)

# Производная: f'(x) = -sin(x + x^3) * (1 + 3x^2)
df = -np.sin(x0 + x0**3) * (1 + 3 * x0**2)

# Уравнение касательной
x_tan = np.linspace(x0 - 0.5, x0 + 0.5, 100)
y_tan = df * (x_tan - x0) + y0

# === Строим график ===
plt.figure(figsize=(10, 6))

# График функции (две части)
plt.plot(x1, y1, 'b-', label=r'$f(x) = \cos(x + x^3)$', linewidth=2)
plt.plot(x2, y2, 'b-', linewidth=2)

# Касательная
plt.plot(x_tan, y_tan, 'r--', label=f'Касательная в $x_0 = {x0}$', linewidth=2)

# Точка касания
plt.scatter([x0], [y0], color='red', zorder=5)
plt.annotate(f'Точка касания ({x0:.1f}; {y0:.2f})',
             xy=(x0, y0),
             xytext=(x0 + 0.3, y0 + 0.4),
             arrowprops=dict(arrowstyle='->', color='red'),
             fontsize=11)

# Оформление
plt.title('График функции и касательной (Вариант 1)', fontsize=14)
plt.xlabel('x', fontsize=12)
plt.ylabel('f(x)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11, loc='best')
plt.axvline(x=1, color='gray', linestyle=':', alpha=0.5)

plt.tight_layout()
plt.savefig('variant1_plot.png', dpi=300, bbox_inches='tight')
plt.show()