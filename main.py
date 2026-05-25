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
emoji = ["🌊", "🚢", "🌊", "🔹", "💥", "❌️"]
# 0 - скрытый корабль 🌊, 
# 1 - открытый корабль 🚢, 
# 2 - скрытая пустышка 🌊, 
# 3 - открытая пустышка 🔸, 
# 4 - попал 💥
# 5 - убит ❌️

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

def add_part_of_ship(ships: list, ship_idx: int, part: list):
    ships[ship_idx].insert(-1, part)
    ships[ship_idx][-1] += 1
    return True

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

def set_ship1(cell1, cell2, field, ships, placement_method=-1):
    # находим offset
    # (1, 0), (-1, 0), (0, 1), (0, -1)
    
    # находим начальные координаты и 
    # изменение для следующей палубы
    dx = (cell2[0] > cell1[0]) - (cell2[0] < cell1[0])
    dy = (cell2[1] > cell1[1]) - (cell2[1] < cell1[1])
    num = max(abs(cell2[0] - cell1[0]), abs(cell2[1] - cell1[1]))
    x, y = list(cell1)

    if placement_method != num:
        return False

    # предпологаем в каких координатах 
    # будет конец корабля

    # если корабль выходит за пределы карты
    if any([cell2[0] < 0, cell2[1] < 0,
            cell2[0] > 9, cell2[1] > 9]):
        return False

    list_for_test = [(-1, -1), (1, 1), (-1, 1), (1, -1),
                  (0, 1), (0, -1), (1, 0), (-1, 0),
                  (0, 0)]
    for i in range(num + 1):
        for j in list_for_test:
            if 0 <= y + dy*i + j[1] <= 9 and 0 <= x + dx*i + j[0] <= 9 and \
                field[y + dy * i + j[1]][x + dx * i + j[0]] in [0, 1, 4, 5]:
                return False

    # создаем новый корабль
    ships.append([0])

    # заменяем каждую клетку которую надо
    # на корабль
    for _ in range(num + 1):
        change_cell([x, y], 0, field)
        add_part_of_ship(ships, -1, [x, y, True])
        x += dx
        y += dy

    return True

# на входе получаем координату только носа корабля,
# направление построения, сколько палуб и само поле
# куда будем его пихать
# coordinate -> cell
# direction -> dir
def set_ship2(cell, dir, num, field, ships, placement_method=-1):    
    # dir принимает udlr и ^v<>
    # для определения смещения dir
    if placement_method != num:
        return False
    
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

    list_for_test = [(-1, -1), (1, 1), (-1, 1), (1, -1),
                  (0, 1), (0, -1), (1, 0), (-1, 0),
                  (0, 0)]
    for i in range(num):
        for j in list_for_test:
            if 0 <= y + dy*i + j[1] <= 9 and 0 <= x + dx*i + j[0] <= 9 and \
                field[y + dy * i + j[1]][x + dx * i + j[0]] in [0, 1, 4, 5]:
                return False

    # создаем новый корабль
    ships.append([0])

    # заменяем каждую клетку которую надо
    # на корабль
    for _ in range(num):
        change_cell([x, y], 0, field)
        add_part_of_ship(ships, -1, [x, y, True])
        x += dx
        y += dy

    return True
    # добавить механику добавления корабля в список 
    # ships_player/bot_has

# нормально сделать чтобы корды были везде через [x, y], 
# а не как попало

# ships = []
# while True:
#     print_field(field)

#     # raw_cell, dir, num = input().split(" ")
#     # cell = [int(i) for i in raw_cell.split(",")]
#     # print(set_ship2(cell, dir, int(num), field, ships))
#     # print(ships)

#     raw_cell1, raw_cell2 = input().split(" ")
#     cell1 = [int(i) for i in raw_cell1.split(",")]
#     cell2 = [int(i) for i in raw_cell2.split(",")]
#     print(set_ship1(cell1, cell2, field, ships))
#     print(ships)

#     time.sleep(5)
#     clear()

# убрать баг при размещении корабль на корабль 
# и столконовение кораблей

if __name__ == "__main__":
    ships = []
    while True:
        print_field(field)

        raw_cell, dir, num = input().split(" ")
        cell = [int(i) for i in raw_cell.split(",")]
        print(set_ship2(cell, dir, int(num), field, ships))

        time.sleep(0.5)
        clear()