zoo = ['lion', 'kangaroo', 'elephant', 'monkey', ]
birds = ['rooster', 'ostrich', 'lark', ]
zoo.insert(1, 'bear')
print(zoo)
zoo.extend(birds)
print(zoo)
zoo.remove('elephant')
print(zoo)
lion_cage=zoo.index('lion') + 1
lark_cage=zoo.index('lark') + 1
print('Лев сидит в', lion_cage)
print('жаворонок сидит в', lark_cage)