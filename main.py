# импорт всех нужных библиотек
import time
import os
import random
import bot
from debug import DEBUG, log
from language import LANGUAGE, msg
import user

# поле для игрока
player_field = [[2 for _ in range(10)] for _ in range(10)]
player_ships = []

# поле где игрок атакует
player_radar = [[2 for _ in range(10)] for _ in range(10)]

# поле бота
bot_field = [[2 for _ in range(10)] for _ in range(10)]
bot_ships = []

# поле где бот атакует
bot_radar = [[2 for _ in range(10)] for _ in range(10)]

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

words = ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К"] if LANGUAGE == "ru" else \
    ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

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
    elif set_ship == "3": # A1
        return [(ru_words_to_parse.index(command[0]) if command[0] in ru_words_to_parse else en_words_to_parse.index(command[0])), 
                int(command[1:]) - 1] # [0, 0]
    

# печатаем поле
def print_field(field1, field2=[-1]):
    log("print_field")

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
    log(f"change_cell, cell = {cell}, num = {num}")
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
    log(f"fire, x = {x}, y = {y}, field[y][x] = {field[y][x]}")
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
    log(f"set_ship1, cell1 = {cell1}, cell2 = {cell2}, num = {num}, method = {placement_method}")
    # находим offset
    # (1, 0), (-1, 0), (0, 1), (0, -1)
    
    # находим начальные координаты и 
    # изменение для следующей палубы
    dx = (cell2[0] > cell1[0]) - (cell2[0] < cell1[0])
    dy = (cell2[1] > cell1[1]) - (cell2[1] < cell1[1])
    steps = max(abs(cell2[0] - cell1[0]), abs(cell2[1] - cell1[1]))
    x, y = list(cell1)
    log(f"dx = {dx}, dy = {dy}, steps = {steps}, x = {x}, y = {y}")

    if placement_method != steps + 1 and placement_method != -1:
        log("корабль не соотвествует размеру метода постановки")
        return False

    # предпологаем в каких координатах 
    # будет конец корабля

    # если корабль выходит за пределы карты
    if any([cell2[0] < 0, cell2[1] < 0,
            cell2[0] > 9, cell2[1] > 9]):
        log("ОШИБКА: корабль не влезает")
        return False

    list_for_test = [(-1, -1), (1, 1), (-1, 1), (1, -1),
                  (0, 1), (0, -1), (1, 0), (-1, 0),
                  (0, 0)]
    for i in range(steps + 1):
        for j in list_for_test:
            if 0 <= y + dy*i + j[1] <= 9 and 0 <= x + dx*i + j[0] <= 9 and \
                field[y + dy * i + j[1]][x + dx * i + j[0]] in [0, 1, 4, 5]:
                log("ОШИБКА: корабль пересекает другой корабль или стоит рядом меньше чем через 1 клетку")
                return False

    # создаем новый корабль
    ships.append([0])
    log("успешное создание")

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
    log(f"set_ship2, cell = {cell}, dir = {dir}, steps = {steps}, num = {num}, method = {placement_method}")
    # dir принимает udlr и ^v<>
    # для определения смещения dir
    if placement_method != steps and placement_method != -1:
        log("корабль не соотвествует размеру метода постановки")
        return False
    
    delta = {
        "v": (0, 1), "d": (0, 1),
        "^": (0, -1), "u": (0, -1),
        "<": (-1, 0), "l": (-1, 0),
        ">": (1, 0), "r": (1, 0)
    }
    # узнаем смещение
    offset = delta.get(dir)
    log(f"offset = {offset}")

    # если неверный ввод
    if offset == None:
        log("неверное направление")
        return False

    # находим начальные координаты и 
    # изменение для следующей палубы
    dx, dy = offset
    x, y = list(cell)
    log(f"x = {x}, y = {y}, dx = {dx}, dy = {dy}")

    # предпологаем в каких координатах 
    # будет конец корабля
    final_x = x + dx * steps
    final_y = y + dy * steps

    # если корабль выходит за пределы карты
    if any([final_x < -1, final_y < -1,
            final_x > 10, final_y > 10]):
        log("ОШИБКА: корабль не влезает")
        return False

    list_for_test = [(-1, -1), (1, 1), (-1, 1), (1, -1),
                  (0, 1), (0, -1), (1, 0), (-1, 0),
                  (0, 0)]
    for i in range(steps):
        for j in list_for_test:
            if 0 <= y + dy*i + j[1] <= 9 and 0 <= x + dx*i + j[0] <= 9 and \
                field[y + dy * i + j[1]][x + dx * i + j[0]] in [0, 1, 4, 5]:
                log("ОШИБКА: корабль пересекает другой корабль или стоит рядом меньше чем через 1 клетку")
                return False

    # создаем новый корабль
    ships.append([0])
    log("успешное создание")

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
    log(f"update, method = {method}")
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

def start(turn, set_ship, bot_name, placement_method, name=-1):
    log(f"start, turn = {turn}, set_ship = {set_ship}, bot_name = {bot_name}, method = {placement_method}")
    # turn = input("select 1st turn (default player): ") or "player"
    # set_ship = input("select set_ship (default 1): ") or "1"
    # bot_name = input("select bot (default harpooner): ") or "harpooner"
    # placement_method = input("select placement method (default 1111222334): ") or "1111222334"
    who_win = "nobody"
    game_mode = "placement" # attacking

    while who_win == "nobody":
        if game_mode == "placement":
            print(msg("player's turn to place ships"))
            for i in list(placement_method):
                print_field(player_field, player_radar)
                if set_ship == "1":
                    while True:
                        cmd = parse(input("> "), "1")
                        # raw_cell1, raw_cell2 = input().split(" ")
                        # cell1 = [int(i) for i in raw_cell1.split(",")]
                        # cell2 = [int(i) for i in raw_cell2.split(",")]

                        if set_ship1(*cmd, player_field, player_ships, 1, int(i)): break
                        else: print("incorrect input")

                elif set_ship == "2":
                    while True:
                        cmd = parse(input("> "), "2")
                        # raw_cell, dir, num = input().split(" ")
                        # cell = [int(i) for i in raw_cell.split(",")]

                        if set_ship2(*cmd, player_field, player_ships, 1, int(i)): break
                        else: print("iccorect input")

                else:
                    print(msg("incorrect set-ship value"))
                    break
                if not DEBUG: os.system("clear")

            print(msg("bot's turn to place ships"))
            time.sleep(0.7)

            bot.set_ships(bot_field, bot_ships, placement_method)

            game_mode = "attacking"
            log("расстановка завершена, режим атаки")

            # добавление bot_field в player_radar
            update(bot_field, player_radar, "to radar")

            # добавление player_field в bot_radar
            update(player_field, bot_radar, "to radar")
        
        if game_mode == "attacking":
            if turn == "player":
                print(msg("player's turn"))
                print_field(player_field, player_radar)
                # print_field(bot_field, bot_radar)

                while True:
                    cmd = parse(input("> "), "3")
                    result = fire(player_radar, cmd)
                    if result[0]:
                        break
                    else: print(msg("incorrect input"))
                
                if not result[1]:
                    log("промах")
                    turn = "bot"
                else:
                    log("попал")
                    # изменение в списке кораблей
                    ship_idx, part_idx = bot.find_ship_by_cell(bot_ships, cell)
                    bot_ships[ship_idx][part_idx][2] = False
                    bot_ships[ship_idx][-1] -= 1

                    # если убит
                    if bot_ships[ship_idx][-1] == 0:
                        log("и убил")
                        bot.clear_ship(player_radar, bot_ships, ship_idx)

                update(player_radar, bot_field, "to field")

                res = True
                for i in player_radar:
                    if 0 in i: res = False
                if res:
                    who_win = "player"

            elif turn == "bot":
                print(msg("bot's turn"))
                time.sleep(0.5)

                if bot_name == "greenhorn":
                    if not bot.greenhorn(bot_radar, player_ships): who_win = "bot"
                elif bot_name == "harpooner":
                    if not bot.harpooner(bot_radar, player_ships): who_win = "bot"
                elif bot_name == "navigator":
                    if not bot.navigator(bot_radar, player_ships): who_win = "bot"
                elif bot_name == "admiral":
                    if not bot.admiral(bot_radar, player_ships): who_win = "bot"
                elif bot_name == "master_seawolf":
                    if not bot.master_seawolf(bot_radar, player_ships, name): who_win = "bot"
                else:
                    print(msg("incorrect bot name"))
                
                turn = "player"

                update(bot_radar, player_field, "to field")
            
            else:
                print(msg("incorrect turn"))
                break
            if not DEBUG: os.system("clear")
    if who_win == "nobody":
        log(f"ошибка: никто не выиграл, who_win = {who_win}")
        print(msg("error"))
        return False

    elif who_win == "bot":
        print(msg("bot won"))
        print_field(player_field, player_radar)
        if name != -1:
            user.add_game(name, bot.get_all_cells_from_ships(player_ships), False)
    elif who_win == "player":
        print(msg("player won"))
        print_field(player_field, player_radar)
        if name != -1:
            user.add_game(name, bot.get_all_cells_from_ships(player_ships), True)
    return True

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
    start("player", "1", "harpooner", "1111222334", "imefo")
#     ships = []
#     while True:
#         print_field(field)

#         raw_cell, dir, num = input().split(" ")
#         cell = [int(i) for i in raw_cell.split(",")]
#         print(set_ship2(cell, dir, int(num), field, ships, 0))

#         time.sleep(0.5)
#         clear()