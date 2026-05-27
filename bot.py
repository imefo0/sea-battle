import random, time, os
from debug import DEBUG, log
# import main

# 0 - скрытый корабль 🌊, 
# 1 - открытый корабль 🚢, 
# 2 - скрытая пустышка 🌊, 
# 3 - открытая пустышка 🔸, 
# 4 - попал 💥
# 5 - убит ❌️

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

# searching - поиск через рандом
# attack - атака
harpooner_mode = "searching"
navigator_mode = "searching"

navigator_map = []


directions = [
    (1, 0), (-1, 0),
    (0, 1), (0, -1)
]
for a in [
    [(0, 1), (0, 5), (0, 9), (4, 9), (8, 9)],
    [(0, 3), (0, 7), (2, 9), (6, 9)]
]:
    navigator_map.append([])
    for i in a:
        x0, y0 = i
        x, y = x0, y0
        while (x, y) != (y0, x0):
            navigator_map[-1].append((x, y))
            x += 1
            y -= 1


def find_ship_by_cell(ships, cell):
    log("find_ship_by_cell")
    x, y = list(cell)
    for ship_idx, ship in enumerate(ships):
        for part_idx, part in enumerate(ship[:-1]):
            if part[0] == x and part[1] == y:
                return ship_idx, part_idx
    log("ОШИБКА: корабль не найден")
    return None, None

def clear_ship(field, ships, ship_idx):
    log("clear_ship")
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
    else:
        log("ОШИБКА: этот корабль не убит")
        return False
    return True

def set_ships(field: list[list[int]], ships, placement_method: list[str]) -> bool:
    log("set_ships")
    list_of_methods = list(map(int, placement_method))
    attempts = 0
    for num in list_of_methods:
        while True:
            while attempts <= 1000:
                attempts += 1
                cell = [random.randint(0, 9), random.randint(0, 9)]
                # узнаем смещение
                offset = random.choice([(0, 1), (0, -1), (-1, 0), (1, 0)])

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

                ok = "ok"

                # если корабль выходит за пределы карты
                if any([final_x < -1, final_y < -1,
                        final_x > 10, final_y > 10]):
                    ok = "continue"

                list_for_test = [(-1, -1), (1, 1), (-1, 1), (1, -1),
                            (0, 1), (0, -1), (1, 0), (-1, 0),
                            (0, 0)]
                
                for i in range(num):
                    for j in list_for_test:
                        if 0 <= y + dy*i + j[1] <= 9 and 0 <= x + dx*i + j[0] <= 9 and \
                            field[y + dy * i + j[1]][x + dx * i + j[0]] in [0, 1, 4, 5]:
                            ok = "continue"
                
                if ok == "continue":
                    ok = "ok"
                    continue

                # создаем новый корабль
                ships.append([0])

                # заменяем каждую клетку которую надо
                # на корабль
                for _ in range(num):
                    field[y][x] = 0
                    
                    ships[-1].insert(-1, [x, y, True])
                    ships[-1][-1] += 1
                    x += dx
                    y += dy
                
                break
            if attempts > 1000:
                log(f"перестановка, попыток: {attempts}")
                field = [[2 for _ in range(10)] for _ in range(10)]
                attempts = 0
            else:
                log("бот поставил корабль")
                break
    return True

def attack_mode(field, ships, bot) -> list[str, bool]: # для harpooner, navigator
    log("attack_mode")
    global directions, harpooner_mode, navigator_mode, x, y
    # import pdb; pdb.set_trace()
    while True:
        if x - 1 < 0 and (-1, 0) in directions: directions.remove((-1, 0))
        if x + 1 > 9 and (1, 0) in directions: directions.remove((1, 0))
        if y - 1 < 0 and (0, -1) in directions: directions.remove((0, -1))
        if y + 1 > 9 and (0, 1) in directions: directions.remove((0, 1))

        # выборка направления
        dx, dy = random.choice(directions) 
        log(f"dx = {dx}, dy = {dy}, directions = {directions}")

        # если попал
        if field[y + dy][x + dx] == 0:
            log("бот попал")
            field[y + dy][x + dx] = 4
            x, y = x + dx, y + dy

            # изменение в списке кораблей
            ship_idx, part_idx = find_ship_by_cell(ships, [x, y])
            ships[ship_idx][part_idx][2] = False
            ships[ship_idx][-1] -= 1

            # удаляем перпендикулярные направления
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

            # если убит
            if ships[ship_idx][-1] == 0:
                log("бот убил")
                clear_ship(field, ships, ship_idx)
                directions = [
                    (1, 0), (-1, 0), (0, 1), (0, -1)
                ]
                if bot == "harpooner":
                    harpooner_mode = "searching"
                elif bot == "navigator":
                    navigator_mode = "searching"
            return ["continue", True]

        # если мимо
        elif field[y + dy][x + dx] == 2:
            log("бот промахнулся")
            field[y + dy][x + dx] = 3
            # если дошли до края корабля но не убили его
            if len(directions) == 1:
                directions.append( (-directions[0][0], -directions[0][1]) )
                del directions[0] 
                return ["break", True]
            directions.remove((dx, dy))
            return ["break", True]

        # если уже стреляли по кораблю (то "ходим" по нему)
        elif field[y + dy][x + dx] == 4:
            log('бот "ходит" по кораблю')
            x, y = x + dx, y + dy
            return ["continue", True]

        elif field[y + dy][x + dx] in [1, 3, 5] and \
            (harpooner_mode == "attack" or navigator_mode == "attack"):
            log("ОШИБКА: бот стреляет в выстреленную клетку")
            directions.remove((dx, dy))
            return ["continue", True]

        return ["break", True]

def greenhorn(field, ships): # юнга, рандом
    log("greenhorn")
    while True:
        res = True
        for i in field:
            if 0 in i: res = False
        if res:
            return False
        # пытаемся стрельнуть в рандомную координату
        x, y = [random.randint(0, 9), random.randint(0, 9)]

        # если попали
        if field[y][x] == 0:
            log("бот попал")
            field[y][x] = 4
    
            # изменение в списке кораблей
            ship_idx, part_idx = find_ship_by_cell(ships, [x, y])
            ships[ship_idx][part_idx][2] = False
            ships[ship_idx][-1] -= 1

            # если убили корабль
            if ships[ship_idx][-1] == 0:
                log("бот убил")
                if not clear_ship(field, ships, ship_idx): return False

        # если промахнулись
        elif field[y][x] == 2:
            log("бот промахнулся")
            field[y][x] = 3
            break

    return True

def harpooner(field, ships): # гаупунер, охотник
    log("harpooner")
    global directions, harpooner_mode, x, y

    while True:
        #import pdb; pdb.set_trace()
        status = True
        for i in field:
            if 0 in i: status = False
        if status:
            return False

        # режим поиска
        if harpooner_mode == "searching":
            log("поиск корабля")

            x, y = [random.randint(0, 9), random.randint(0, 9)]
            
            # если попали
            if field[y][x] == 0:
                log("бот попал")
                field[y][x] = 4

                # измененить список кораблей
                ship_idx, part_idx = find_ship_by_cell(ships, [x, y])
                ships[ship_idx][part_idx][2] = False
                ships[ship_idx][-1] -= 1
                
                # если убили
                if ships[ship_idx][-1] == 0:
                    log("бот убил корабль")
                    clear_ship(field, ships, ship_idx)
                    directions = [
                        (1, 0), (-1, 0), (0, 1), (0, -1)
                    ]
                    harpooner_mode = "searching"
                    x, y = None, None

                    continue

                harpooner_mode = "attack"

                continue

            # если мимо
            elif field[y][x] == 2:
                log("бот промахнулся")
                field[y][x] = 3
                directions = [
                (0, 1), (1, 0), (0, -1), (-1, 0)
                ]
                break
    
        elif harpooner_mode == "attack":
            log("бот уже нашел корабль и атакует")
            result = attack_mode(field, ships, "harpooner")
            if result[1]:
                if result[0] == "continue":
                    continue
                elif result[0] == "break":
                    break
    return True

def navigator(field, ships): # штурман, шахматный
    log("navigator")
    global directions, navigator_mode, x, y

    while True:
        #import pdb; pdb.set_trace()
        status = True
        for i in field:
            if 0 in i: status = False
        if status:
            return False

        # режим поиска
        if navigator_mode == "searching":
            log("бот ищет корабль")
            if [] in navigator_map:
                navigator_map.remove([])
            if navigator_map == []:
                x, y = random.randint(0, 9), random.randint(0, 9)
            if navigator_map != [] and [] not in navigator_map:
                x, y = random.choice(navigator_map[0])
                navigator_map[0].remove((x, y))
            
            # если попали
            if field[y][x] == 0:
                log("бот попал")
                field[y][x] = 4

                # измененить список кораблей
                ship_idx, part_idx = find_ship_by_cell(ships, [x, y])
                ships[ship_idx][part_idx][2] = False
                ships[ship_idx][-1] -= 1
                
                # если убили
                if ships[ship_idx][-1] == 0:
                    log("бот убил")
                    clear_ship(field, ships, ship_idx)
                    directions = [
                        (1, 0), (-1, 0), (0, 1), (0, -1)
                    ]
                    navigator_mode = "searching"
                    x, y = None, None

                    continue

                navigator_mode = "attack"

                continue

            # если мимо
            elif field[y][x] == 2:
                log("бот промахнулся")
                field[y][x] = 3
                directions = [
                (0, 1), (1, 0), (0, -1), (-1, 0)
                ]
                break
        
        elif navigator_mode == "attack":
            log("бот уже нашел корабль и идет атаковать")
            result = attack_mode(field, ships, "navigator")
            if result[1]:
                if result[0] == "continue":
                    continue
                elif result[0] == "break":
                    break
    return True

def admiral(field, ships): # адмирал, тепловая карта
    log("адмирал")
    while True:
        res = True
        for i in field:
            if 0 in i: res = False
        if res:
            return False
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
        log("бот считает клетки")
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
            log("бот попал")
            field[y][x] = 4

            # изменение в списке кораблей
            ship_idx, part_idx = find_ship_by_cell(ships, [x, y])
            ships[ship_idx][part_idx][2] = False
            ships[ship_idx][-1] -= 1

            # если убили корабль
            if ships[ship_idx][-1] == 0:
                log("бот убил")
                for i in range(len(ships[ship_idx]) - 1):
                    ship = ships[ship_idx][i]
                    heat_map[ship[1]][ship[0]] = 0
                clear_ship(field, ships, ship_idx)
            continue
        elif field[y][x] == 2:
            log("бот промахнулся")
            field[y][x] = 3
            heat_map[y][x] = 0
            break
        else: 
            log("ОШИБКА: в эту клетку уже стреляли")
            del pos[point]
            continue
    return True

def master_seawolf(field): # мастер Морской волк, карта + история
    log("master_seawolf")
    pass

# В играх сложность ботов обычно строится как «слоеный пирог»:
# каждый следующий уровень включает в себя фишки предыдущего.

if __name__ == "__main__":
    import main
    ships = []

    main.set_ship1([1,1], [1,1], main.field, ships, 0, 1)
    main.set_ship1([3,2], [5,2], main.field, ships, 0, 3)
    main.set_ship1([7,2], [8,2], main.field, ships, 0, 2)
    main.set_ship1([1,3], [1,4], main.field, ships, 0, 2)
    main.set_ship1([3,4], [6,4], main.field, ships, 0, 4)

    main.set_ship1([8,4], [8,5], main.field, ships, 0, 2)
    main.set_ship1([1,6], [3,6], main.field, ships, 0, 3)
    main.set_ship1([5,6], [5,6], main.field, ships, 0, 1)
    main.set_ship1([7,7], [7,7], main.field, ships, 0, 1)
    main.set_ship1([4,8], [4,8], main.field, ships, 0, 1)

    os.system("clear")
    num = 1

    while True:
        status = admiral(main.field, ships)
        n = 0
        for i in range(len(main.field)):
            for j in range(len(main.field[i])):
                if main.field[i][j] in [1, 3, 4, 5]:
                    n += 1
        if status:
            print(f"адмирал делает ход {num}...")
            print(f"|{int(n/2)*"#"}{(50 - int(n/2))*" "}| {n}% {n}/100")
            main.print_field(main.field, main.field)
            # input()
            time.sleep(0.1)
            os.system("clear")
            num += 1
        else:
            print(f"адмирал победил за ходов: {num}!")
            print(f"|{int(n/2)*"#"}{(50 - int(n/2))*" "}| {n}% {n}/100")
            main.print_field(main.field, main.field)
            break

# if __name__ == "__main__":
#     import main
#     ships = []
#     set_ships(main.field, ships, [1,1,1,1,2,2,2,3,3,4])
#     main.print_field(main.field)