import random, time, os
import main

# 0 - скрытый корабль 🌊, 
# 1 - открытый корабль 🚢, 
# 2 - скрытая пустышка 🌊, 
# 3 - открытая пустышка 🔸, 
# 4 - попал 💥
# 5 - убит 💀

# пример ships:
# [ 
#   [[3, 0, True], [3, 1, False], [3, 2, False], 1], 
#   [[0, 1, True], [1, 1, True], 2],
#   [[9, 9, False], 0]
# ] - три корабля:
# первый корабль - корабль с Г1 до Г3, где одна палуба жива (Г1)
# второй корабль - корабль с А2 до Б2, полностью жив
# третий корабль - корабль на К9, мертв

# searching - поиск через рандом
# attack - атака
harpooner_mode = "searching"
cells = []
directions = [
    (1, 0), (-1, 0),
    (0, 1), (0, -1)
]

def find_ship_by_cell(ships, cell):
    x, y = list(cell)
    for ship_idx, ship in enumerate(ships):
        for part_idx, part in enumerate(ship[:-1]):
            if part[0] == x and part[1] == y:
                return ship_idx, part_idx
    return None, None

def clear_ship(field, ships, ship_idx):
    ship = ships[ship_idx]
    if ships[ship_idx][-1] == 0:
        for part in ship:
            if isinstance(part, list):
                x, y, _ = part
                field[y][x] = 5

    else: return False
    return True

def greenhorn(field, ships): # юнга, рандом
    while True:
        # пытаемся стрельнуть в рандомную координату
        x, y = [random.randint(0, 9), random.randint(0, 9)]

        # если попали
        if field[y][x] == 0:
            field[y][x] = 4
    
            # изменение в списке кораблей
            ship_idx, part_idx = find_ship_by_cell(ships, [x, y])
            ships[ship_idx][part_idx][2] = False
            ships[ship_idx][-1] -= 1

            # если убили корабль
            if ships[ship_idx][-1] == 0:
                if not clear_ship(field, ships, ship_idx): return False

        # если промахнулись
        elif field[y][x] == 2:
            field[y][x] = 3
            break

    return True

def harpooner(field, ships): # гаупунер, охотник
    global directions, harpooner_mode, cells, x, y

    # повторять бесконечно:
    while True:
        # import pdb; pdb.set_trace()
        # если режим поиска, то
        if harpooner_mode == "searching":
            # выбираем случайное число для x, y от 0 до 9
            x, y = [random.randint(0, 9), random.randint(0, 9)]
            # если попали, то
            if field[y][x] == 0:
                field[y][x] = 4

                # измененить список кораблей
                ship_idx, part_idx = find_ship_by_cell(ships, [x, y])
                ships[ship_idx][part_idx][2] = False
                ships[ship_idx][-1] -= 1
                
                # если убили, то
                if ships[ship_idx][-1] == 0:
                    clear_ship(field, ships, ship_idx)
                    directions = [
                        (1, 0), (-1, 0), (0, 1), (0, -1)
                    ]
                    cells.clear()
                    harpooner_mode = "searching"
                    x, y = None, None
                    break
                cells.append([x, y])
                harpooner_mode = "attack"
#             продолжить
                continue

#         иначе если мимо, то
            if field[y][x] == 2:
                field[y][x] = 3
#             прервать
                break
    
#     иначе если режим атаки, то
        if harpooner_mode == "attack":
            if x - 1 < 0: directions.remove((-1, 0))
            if x + 1 > 9: directions.remove((1, 0))
            if y - 1 < 0: directions.remove((0, -1))
            if y + 1 > 9: directions.remove((0, 1))
#         (оставить, но без dx и dy)
#         если x + dx < 0, то удалить напраление (-1, 0)
#         если x + dx > 9, то удалить направление (1, 0)
#         если y + dy < 0, то удалить направление (0, -1)
#         если y + dy > 9, то удалить направление (0, 1)
            # if len(directions) == 0:
                # exit("len(direction) = 0")
            dx, dy = random.choice(directions)
#         выбираем случайное направление
#         dx, dy равен случайному направлению

            if field[y + dy][x + dx] == 0:
                field[y + dy][x + dx] = 4
                x, y = x+dx, y+dy
                cells.append([x, y])
#         стреляем в клетку [x+dx, y+dy]
#         если попали в клетку, то
#             добавить [x+dx, y+dy] в клетки

#             изменить список кораблей
                ship_idx, part_idx = find_ship_by_cell(ships, [x, y])
                ships[ship_idx][part_idx][2] = False
                ships[ship_idx][-1] -= 1
#             (делать через словарь)
#             если направление (1, 0) или (-1, 0), то
                if dx != 0:
                    if (0, 1) in directions:
                        directions.remove((0, 1))
                    if (0, -1) in directions: 
                        directions.remove((0, -1))
                if dy != 0:
                    if (1, 0) in directions:
                        directions.remove((1, 0))
                    if (-1, 0) in directions: 
                        directions.remove((-1, 0))
#                 удалить (0, 1) и (0, -1)
#             иначе если направлеие по y, то
#                 удалить по аналогии, удалить направления по x
                
#             если убили, то
#                 сменить корабль на убитый
#                 теперь режим поиска
#                 сбросить направления и клетки
                if ships[ship_idx][-1] == 0:
                    clear_ship(field, ships, ship_idx)
                    directions = [
                        (1, 0), (-1, 0), (0, 1), (0, -1)
                    ]
                    cells.clear()
                    harpooner_mode = "searching"
                    x, y = None, None
                    break
#         (необязательно)
#         если попали в уже атакованную клетку, то продолжить
            elif field[y + dy][x + dx] == 2:
                field[y + dy][x + dx] = 3
                directions.remove((dx, dy))
                break
#         если мимо, то
#             удалить данное направление
#             прервать
# вернуть да
    return True

def navigator(field): # штурман, шахматный
    pass

def admiral(field): # адмирал, тепловая карта
    pass

def master_seawolf(field): # мастер Морской волк, карта + история
    pass

# В играх сложность ботов обычно строится как «слоеный пирог»:
# каждый следующий уровень включает в себя фишки предыдущего.

ships = []

main.set_ship1([1,1], [1,1], main.field, ships)
main.set_ship1([3,2], [5,2], main.field, ships)
main.set_ship1([7,2], [8,2], main.field, ships)
main.set_ship1([1,3], [1,4], main.field, ships)
main.set_ship1([3,4], [6,4], main.field, ships)

main.set_ship1([8,4], [8,5], main.field, ships)
main.set_ship1([1,6], [3,6], main.field, ships)
main.set_ship1([5,6], [5,6], main.field, ships)
main.set_ship1([7,7], [7,7], main.field, ships)
main.set_ship1([4,8], [4,8], main.field, ships)

os.system("clear")
num = 0

while True:
    harpooner(main.field, ships)
    print(f"охотник делает ход {num}...")
    main.print_field(main.field)
    # time.sleep(0.5)
    # os.system("clear")
    num += 1