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

    while True:
        #import pdb; pdb.set_trace()
        status = True
        for i in field:
            if 0 in i: status = False
        if status:
            return False

        # режим поиска
        if harpooner_mode == "searching":

            x, y = [random.randint(0, 9), random.randint(0, 9)]
            
            # если попали
            if field[y][x] == 0:
                field[y][x] = 4

                # измененить список кораблей
                ship_idx, part_idx = find_ship_by_cell(ships, [x, y])
                ships[ship_idx][part_idx][2] = False
                ships[ship_idx][-1] -= 1
                
                # если убили
                if ships[ship_idx][-1] == 0:
                    clear_ship(field, ships, ship_idx)
                    directions = [
                        (1, 0), (-1, 0), (0, 1), (0, -1)
                    ]
                    cells.clear()
                    harpooner_mode = "searching"
                    x, y = None, None

                    continue

                cells.append([x, y])
                harpooner_mode = "attack"

                continue

            # если мимо
            elif field[y][x] == 2:
                field[y][x] = 3
                directions = [
                (0, 1), (1, 0), (0, -1), (-1, 0)
                ]
                break
    
        # режим атаки
        elif harpooner_mode == "attack":

            if x - 1 < 0: directions.remove((-1, 0))
            if x + 1 > 9: directions.remove((1, 0))
            if y - 1 < 0: directions.remove((0, -1))
            if y + 1 > 9: directions.remove((0, 1))

            # выборка направления
            dx, dy = random.choice(directions) 

            # если попал
            if field[y + dy][x + dx] == 0:
                field[y + dy][x + dx] = 4
                x, y = x + dx, y + dy
                cells.append([x, y])

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
                    clear_ship(field, ships, ship_idx)
                    directions = [
                        (1, 0), (-1, 0), (0, 1), (0, -1)
                    ]
                    cells.clear()
                    harpooner_mode = "searching"
                    x, y = None, None
                    continue
            
            # если мимо
            elif field[y + dy][x + dx] == 2:
                field[y + dy][x + dx] = 3
                # если дошли до края корабля но не убили его
                if len(directions) == 1:
                    directions.append( (-directions[0][0], (-directions[0][1])) )
                    del directions[0] 
                    break
                directions.remove((dx, dy))
                break

            # если уже стреляли по кораблю (то "ходим" по нему)
            elif field[y + dy][x + dx] == 4:
                x, y = x + dx, y + dy
                continue
    return True

def navigator(field): # штурман, шахматный
    pass

def admiral(field): # адмирал, тепловая карта
    pass

def master_seawolf(field): # мастер Морской волк, карта + история
    pass

# В играх сложность ботов обычно строится как «слоеный пирог»:
# каждый следующий уровень включает в себя фишки предыдущего.
if __name__ == "__main__":
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
        status = list(harpooner(main.field, ships))
        if status[0]:
            print(f"охотник делает ход {num}...")
            main.print_field(main.field)
            print(f"{status[1]}")
            # input()
            # time.sleep(2)
            # os.system("clear")
            num += 1
        else:
            print("охотник победил!")
            break