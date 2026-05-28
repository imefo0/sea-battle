# импорт всех нужных библиотек
import time
import os
import random
import bot

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

en_words_to_parse = list("abcdefghij")
ru_words_to_parse = list("абвгдежзик")

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

def parse(command: str, set_ship: str):
    if set_ship == "1": # "A1 J4"
        cmds = command.lower().split(" ") # ["a1" "j4"]
        result = []
        for x in cmds:
            cmds[cmds.index(x)] = [cmds[cmds.index(x)][0], cmds[cmds.index(x)][1:]]
            # [["a", "1"], ["j", "4"]]
        for i in cmds: # ["a", "1"] ["j", "4"]
            result.append([])
            for j in i: # a 1 j 4
                if j.isdigit():
                    result[-1].append(int(j) - 1)
                else:
                    if j in ru_words_to_parse: result[-1].append(ru_words_to_parse.index(j))
                    elif j in en_words_to_parse: result[-1].append(en_words_to_parse.index(j))
        return result
    elif set_ship == "2": # "A1 > 5"
        cmds = command.split(" ") # ["A1", ">", "5"]
        cmds[0] = cmds[0].lower() # ["a1", ">", "5"]
        cmds[0] = [cmds[0][0], int(cmds[0][1:])]
        if cmds[0][0] in ru_words_to_parse: cmds[0][0] = ru_words_to_parse.index(cmds[0][0])
        elif cmds[0][0] in en_words_to_parse: cmds[0][0] = en_words_to_parse.index(cmds[0][0])
        cmds[-1] = int(cmds[-1])
        cmds[0][1] = int(cmds[0][1]) - 1
        return cmds # [[0, 0], ">", 5]
    

# печатаем поле
def print_field(field1, field2=[-1]):
    words = ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К"]

    # пишем все вертикали в виде букв
    print(end="   ")
    for n in range(2 if field2 != [-1] else 1):
        for i in words:
            print(i, end="  ")
        print("\t", end="   ")
    print()

    # перебор в списке поля
    for i in range(len(field1)):
        # пишем пробел, горизонталь, если это i=9 то
        # не пишем перед ним пробел
        print(f" {i+1}" if i != 9 else f"{i+1}", end=" ")
        # пишем каждую клетку
        for j in field1[i]:
            print(translate_to_emoji(j), end=" ")
        if field2 != [-1]:
            print("\t", end="")
            print(f" {i+1}" if i != 9 else f"{i+1}", end=" ")
            for j in field2[i]:
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

def fire(field, cell):
    x, y = cell
    # если в клетку, которую мы стреляли является 
    # скрытым корабликом то меняем на огонь
    if field[y][x] == 0:
        field[y][x] = 4
        return [True, True]
    
    # если скрытая пустышка то меняем на открытую
    elif field[y][x] == 2:
        field[y][x] = 3
        return [True, False]

    else:
        return [False, True]

def set_ship1(cell1, cell2, field, ships, num, placement_method=-1):
    # находим offset
    # (1, 0), (-1, 0), (0, 1), (0, -1)
    
    # находим начальные координаты и 
    # изменение для следующей палубы
    dx = (cell2[0] > cell1[0]) - (cell2[0] < cell1[0])
    dy = (cell2[1] > cell1[1]) - (cell2[1] < cell1[1])
    steps = max(abs(cell2[0] - cell1[0]), abs(cell2[1] - cell1[1]))
    x, y = list(cell1)

    if placement_method != steps + 1 and placement_method != -1:
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
    for i in range(steps + 1):
        for j in list_for_test:
            if 0 <= y + dy*i + j[1] <= 9 and 0 <= x + dx*i + j[0] <= 9 and \
                field[y + dy * i + j[1]][x + dx * i + j[0]] in [0, 1, 4, 5]:
                return False

    # создаем новый корабль
    ships.append([0])

    # заменяем каждую клетку которую надо
    # на корабль
    for _ in range(steps + 1):
        change_cell([x, y], num, field)
        add_part_of_ship(ships, -1, [x, y, True])
        x += dx
        y += dy

    return True

# на входе получаем координату только носа корабля,
# направление построения, сколько палуб и само поле
# куда будем его пихать
# coordinate -> cell
# direction -> dir
def set_ship2(cell, dir, steps, field, ships, num, placement_method=-1):
    # dir принимает udlr и ^v<>
    # для определения смещения dir
    if placement_method != steps and placement_method != -1:
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
    final_x = x + dx * steps
    final_y = y + dy * steps

    # если корабль выходит за пределы карты
    if any([final_x < -1, final_y < -1,
            final_x > 10, final_y > 10]):
        return False

    list_for_test = [(-1, -1), (1, 1), (-1, 1), (1, -1),
                  (0, 1), (0, -1), (1, 0), (-1, 0),
                  (0, 0)]
    for i in range(steps):
        for j in list_for_test:
            if 0 <= y + dy*i + j[1] <= 9 and 0 <= x + dx*i + j[0] <= 9 and \
                field[y + dy * i + j[1]][x + dx * i + j[0]] in [0, 1, 4, 5]:
                return False

    # создаем новый корабль
    ships.append([0])

    # заменяем каждую клетку которую надо
    # на корабль
    for _ in range(steps):
        change_cell([x, y], num, field)
        add_part_of_ship(ships, -1, [x, y, True])
        x += dx
        y += dy

    return True
    # добавить механику добавления корабля в список 
    # ships_player/bot_has

def update(field1, field2, method):
    for i in range(len(field1)):
        for j in range(len(field1[i])):
            if method == "to radar":
                if field1[i][j] == 1:
                    field2[i][j] = 0
                elif field1[i][j] == 2:
                    field2[i][j] = 2
                else:
                    field2[i][j] = field1[i][j] 
            elif method == "to field":
                if field1[i][j] == 0:
                    field2[i][j] = 1
                elif field1[i][j] == 2:
                    field2[i][j] = 2
                else:
                    field2[i][j] = field1[i][j]
            else: return False
    return True

def start():
    turn = input("select 1st turn (default player): ") or "player"
    set_ship = input("select set_ship (default 1): ") or "1"
    bot_name = input("select bot (default harpooner): ") or "harpooner"
    placement_method = input("select placement method (default 1111222334): ") or "1111222334"
    who_win = "nobody"
    game_mode = "placement" # attacking

    while who_win == "nobody":
        if game_mode == "placement":
            print("player's turn to place ships")
            for i in list(placement_method):
                print_field(player_field, player_radar)
                if set_ship == "1":
                    while True:
                        cmd = parse(input(), "1")
                        # raw_cell1, raw_cell2 = input().split(" ")
                        # cell1 = [int(i) for i in raw_cell1.split(",")]
                        # cell2 = [int(i) for i in raw_cell2.split(",")]

                        if set_ship1(*cmd, player_field, player_ships, 1, int(i)): break
                        else: print("incorrect input")

                elif set_ship == "2":
                    while True:
                        cmd = parse(input(), "2")
                        # raw_cell, dir, num = input().split(" ")
                        # cell = [int(i) for i in raw_cell.split(",")]

                        if set_ship2(*cmd, player_field, player_ships, 1, int(i)): break
                        else: print("iccorect input")

                else:
                    print("incorrect set_ship")
                    break
                os.system("clear")

            print("bot's turn to place ships")
            time.sleep(0.7)

            bot.set_ships(bot_field, bot_ships, placement_method)

            game_mode = "attacking"

            # добавление bot_field в player_radar
            update(bot_field, player_radar, "to radar")

            # добавление player_field в bot_radar
            update(player_field, bot_radar, "to radar")
        
        if game_mode == "attacking":
            if turn == "player":
                print("player's turn")
                print_field(player_field, player_radar)
                # print_field(bot_field, bot_radar)

                while True:
                    cell = [int(i) for i in input().split(",")]
                    result = fire(player_radar, cell)
                    if result[0]:
                        break
                    else: print("incorrect input")
                
                if not result[1]:
                    turn = "bot"
                else:
                    # изменение в списке кораблей
                    ship_idx, part_idx = bot.find_ship_by_cell(bot_ships, cell)
                    bot_ships[ship_idx][part_idx][2] = False
                    bot_ships[ship_idx][-1] -= 1

                    # если убит
                    if bot_ships[ship_idx][-1] == 0:
                        bot.clear_ship(player_radar, bot_ships, ship_idx)

                update(player_radar, bot_field, "to field")

                res = True
                for i in player_radar:
                    if 0 in i: res = False
                if res:
                    who_win = "player"

            elif turn == "bot":
                print("bot's turn.", end="\r")
                time.sleep(0.3)
                print("bot's turn..", end="\r")
                time.sleep(0.3)
                print("bot's turn...", end="\r")
                time.sleep(0.3)
                print()

                if bot_name == "greenhorn":
                    if not bot.greenhorn(bot_radar, player_ships): who_win = "bot"
                elif bot_name == "harpooner":
                    if not bot.harpooner(bot_radar, player_ships): who_win = "bot"
                elif bot_name == "navigator":
                    if not bot.navigator(bot_radar, player_ships): who_win = "bot"
                elif bot_name == "admiral":
                    if not bot.admiral(bot_radar, player_ships): who_win = "bot"
                elif bot_name == "master_seawolf":
                    print("master_seawolf doesn't work now")
                else:
                    print("incorrect bot name")
                
                turn = "player"

                update(bot_radar, player_field, "to field")
            
            else:
                print("incorrect turn")
                break
            os.system("clear")
    if who_win == "nobody":
        print("error")
        return False

    elif who_win == "bot":
        print("bot won!")
    elif who_win == "player":
        print("player won!")
    return True

# нормально сделать чтобы корды были везде через [x, y], 
# а не как попало

# ships = []
# while True:
#     print_field(field)

#     # raw_cell, dir, num = input().split(" ")
#     # cell = [int(i) for i in raw_cell.split(",")]
#     # print(set_ship2(cell, dir, int(num), field, ships, 0))
#     # print(ships)

#     raw_cell1, raw_cell2 = input().split(" ")
#     cell1 = [int(i) for i in raw_cell1.split(",")]
#     cell2 = [int(i) for i in raw_cell2.split(",")]
#     print(set_ship1(cell1, cell2, field, ships, 0))
#     print(ships)

#     time.sleep(5)
#     clear()

# убрать баг при размещении корабль на корабль 
# и столконовение кораблей

if __name__ == "__main__":
    player_field = create_field()
    player_radar = create_field()
    bot_field = create_field()
    bot_radar = create_field()
    start()
#     ships = []
#     while True:
#         print_field(field)

#         raw_cell, dir, num = input().split(" ")
#         cell = [int(i) for i in raw_cell.split(",")]
#         print(set_ship2(cell, dir, int(num), field, ships, 0))

#         time.sleep(0.5)
#         clear()