
garden = ('ромашка', 'роза', 'одуванчик', 'ромашка', 'гладиолус', 'подсолнух', 'роза', )

meadow = ('клевер', 'одуванчик', 'ромашка', 'клевер', 'мак', 'одуванчик', 'ромашка', )

garden_set = set(garden)
meadow_set = set(meadow)
flower_set = set.union(garden_set,meadow_set)
print(flower_set)
flower_set = garden_set & meadow_set
print(flower_set)
flower_set = garden_set - meadow_set
print(flower_set)
flower_set = meadow_set - garden_set
print(flower_set)