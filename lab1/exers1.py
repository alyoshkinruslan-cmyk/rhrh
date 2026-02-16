import math
radius = 42
pi = float(3.1415926)

S = pi * radius ** 2
print(round(S, 4))

point_1 = (23, 34)

x1, y1 = point_1
distance1 = (x1 ** 2 + y1 ** 2) ** 0.5
print(distance1 <= radius)
point_2 = (30, 30)
x2, y2 = point_2
distance2 = (x2 ** 2 + y2 ** 2) ** 0.5
print(distance2 <= radius)