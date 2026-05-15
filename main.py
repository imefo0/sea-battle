# импорт всех нужных библиотек
import time
import os
import random

# ВЕЗДЕ [x, y], НИКАКОГО xy И ДРУГОЙ ЧУШИ!!!!!!!

# поле для игрока
player_field = []
player_ships = []

# поле где игрок атакует
player_radar = []

# поле бота
bot_field = []
bot_ships = []

# поле где бот атакует
bot_radar = []

# само поле из скрытых пустышек
field = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]

# перечисление эмоджи
emoji = ["🌊", "🚢", "🌊", "🔹", "💥", "💀"]
# 0 - скрытый корабль 🌊, 
# 1 - открытый корабль 🚢, 
# 2 - скрытая пустышка 🌊, 
# 3 - открытая пустышка 🔸, 
# 4 - попал 💥
# 5 - убит 💀

def clear():
    os.system("clear")

# перевод в эмоджи
def translate_to_emoji(num):
    return emoji[num]

# перевод в y через буквы
def translate_from_word(word):
    words = ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К"]
    return words.index(word.capitalize())

# перевод из y в буквы
def translate_to_num(list):
    return f"{''.join(map(str, list))}"

def create_field():
    return [[2 for _ in range(10)] for _ in range(10)]


# печатаем поле
def print_field(field):
    words = ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К"]

    # пишем все вертикали в виде букв
    print(end="   ")
    for i in words:
        print(i, end="  ")
    print()

    # перебор в списке поля
    for i in range(len(field)):
        # пишем пробел, горизонталь, если это i=9 то
        # не пишем перед ним пробел
        print(f" {i+1}" if i != 9 else f"{i+1}", end=" ")
        # пишем каждую клетку
        for j in field[i]:
            print(translate_to_emoji(j), end=" ")
        print()

# сменить ячейку
def change_cell(cell, num, field):
    # выбираем field[y][x] и меняем на c_p_n[2]
    field[cell[1]][cell[0]] = num

# расставить случайно клетки
def randomize():
    for i in range(len(field)):
        for j in range(len(field[i])):
            # берем кажду клетку и ставим либо 0 либо 2
            field[i][j] = random.choice([0, 2])

def fire(cell):
    x, y = cell
    # если в клетку, которую мы стреляли является 
    # скрытым корабликом то меняем на огонь
    if field[y][x] == 0:
        field[y][x] = 4
    
    # если скрытая пустышка то меняем на открытую
    elif field[y][x] == 2:
        field[y][x] = 3

    else:
        return False
    
    return True

def set_ship1(cell1, cell2, field):
    dx = abs(cell1[0] - cell2[0])
    dy = abs(cell1[1] - cell2[1])

    if dx != 0 and dy != 0: return False

    axis = 1 if dx == 0 else 0
    steps = dy if dx == 0 else dx

    cell = list(cell1 if cell1[axis] < cell2[axis] else cell2)

    for _ in range(steps + 1):
        change_cell(cell, 0, field)
        cell[axis] += 1
    
    return True

# на входе получаем координату только носа корабля,
# направление построения, сколько палуб и само поле
# куда будем его пихать
# coordinate -> cell
# direction -> dir
def set_ship2(cell, dir, num, field):    
    # dir принимает udlr и ^v<>
    # для определения смещения dir
    delta = {
        "v": (0, 1), "d": (0, 1),
        "^": (0, -1), "u": (0, -1),
        "<": (-1, 0), "l": (-1, 0),
        ">": (1, 0), "r": (1, 0)
    }
    # узнаем смещение
    offset = delta.get(dir)

    # если неверный ввод
    if offset == None: return False

    # находим начальные координаты и 
    # изменение для следующей палубы
    dx, dy = offset
    x, y = list(cell)

    # предпологаем в каких координатах 
    # будет конец корабля
    final_x = x + dx * num
    final_y = y + dy * num

    # если корабль выходит за пределы карты
    if any([final_x < -1, final_y < -1,
            final_x > 10, final_y > 10]):
        return False

    # заменяем каждую клетку которую надо
    # на корабль
    for _ in range(num):
        change_cell([x, y], 0, field)
        x += dx
        y += dy

    return True
    # добавить механику добавления корабля в список 
    # ships_player/bot_has

# нормально сделать чтобы корды были везде через [x, y], 
# а не как попало
while True:
    print_field(field)

    #raw_cell, dir, num = input().split(" ")
    #cell = [int(i) for i in raw_cell.split(",")]
    #print(set_ship2(cell, dir, int(num), field))

    raw_cell1, raw_cell2 = input().split(" ")
    cell1 = [int(i) for i in raw_cell1.split(",")]
    cell2 = [int(i) for i in raw_cell2.split(",")]
    print(set_ship1(cell1, cell2, field))

    time.sleep(0.5)
    clear()