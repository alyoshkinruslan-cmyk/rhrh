import math

sites = {
    'Moscow': (550, 370),
    'London': (510, 510),
    'Paris': (480, 480),
}
distances = {}


for city1, (x1, y1) in sites.items():
    distances[city1] = {}
for city2, (x2, y2) in sites.items():
    distances[city1][city2] = math.hypot(x1 - x2, y1 - y2)

print(distances)
