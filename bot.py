import random, time, os
import main

# 0 - скрытый корабль 🌊, 
# 1 - открытый корабль 🚢, 
# 2 - скрытая пустышка 🌊, 
# 3 - открытая пустышка 🔸, 
# 4 - попал 💥
# 5 - убит ❌️

# пример ships:
# [ 
#   [[3, 0, True], [3, 1, False], [3, 2, False], 1], 
#   [[0, 1, True], [1, 1, True], 2],
#   [[9, 9, False], 0]
# ] - три корабля:
# первый корабль - корабль с Г1 до Г3, где одна палуба жива (Г1)
# второй корабль - корабль с А2 до Б2, полностью жив
# третий корабль - корабль на К9, мертв

heat_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                    if 0 <= y + dy <= 9 and 0 <= x + dx <= 9:
                        if field[y + dy][x + dx] == 2: 
                            field[y + dy][x + dx] = 3
    else: return False
    return True

def greenhorn(field, ships): # юнга, рандом
    while True:
        # выбор рандомных координат
        x, y = [random.randint(0, 9), random.randint(0, 9)]

        # стреляем
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

        # если мимо
        elif field[y][x] == 2:
            field[y][x] = 3
            break

    return True

def harpooner(field): # гаупунер, охотник
    pass

def navigator(field): # штурман, шахматный
    pass

def admiral(field, ships): # адмирал, тепловая карта
    while True:
        for len_ship in [2, 3, 4]:
            for dx, dy in [(1, 0), (0, 1)]:
                for y in range(0, 10):
                    for x in range(0, 10):
                        status = True
                        for i in range(0, len_ship):
                            nx, ny = x + dx*i, y + dy*i
                            if not (0 <= nx < 10 and 0 <= ny < 10):
                                status = False
                                break
                            if field[ny][nx] not in (0, 2, 4):
                                status = False
                                break
                        if status:
                            for i in range(0, len_ship):
                                if field[y + dy * i][x + dx * i] != 4:
                                    heat_map[y + dy * i][x + dx * i] += 1
        
        max_val = max(max(row) for row in heat_map)
        pos = []

        for y in range(0, 10):
            for x in range(0, 10):
                if heat_map[y][x] == max_val:
                    pos.append([x, y])

        point = random.randint(0, len(pos) - 1)
        x, y = pos[point]

        if field[y][x] == 0:
            field[y][x] = 4

            # изменение в списке кораблей
            ship_idx, part_idx = find_ship_by_cell(ships, [x, y])
            ships[ship_idx][part_idx][2] = False
            ships[ship_idx][-1] -= 1

            # если убили корабль
            if ships[ship_idx][-1] == 0:
                for i in range(len(ships[ship_idx]) - 1):
                    ship = ships[ship_idx][i]
                    heat_map[ship[1]][ship[0]] = 0
                if not clear_ship(field, ships, ship_idx): return False

            continue
        elif field[y][x] == 2:
            field[y][x] = 3
            heat_map[y][x] = 0
            break
        else: 
            del pos[point]
            continue
    return True

def master_seawolf(field): # мастер Морской волк, карта + история
    pass

# В играх сложность ботов обычно строится как «слоеный пирог»:
# каждый следующий уровень включает в себя фишки предыдущего.
