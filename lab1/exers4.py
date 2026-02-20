my_family = ["Отец", "Мать", "Я"]
my_family_height = [
["Отец", 180],
["Мать", 165],
["Я", 175],
]
print(my_family_height[0][1], "см")
total_height = (
my_family_height[0][1]
+ my_family_height[1][1]
+ my_family_height[2][1]
)

print("Общий рост моей семьи =", total_height, "см")