import random, time, os
import main

# 0 - скрытый корабль 🌊, 
# 1 - открытый корабль 🚢, 
# 2 - скрытая пустышка 🌊, 
# 3 - открытая пустышка 🔸, 
# 4 - попал 💥
# 5 - убит 💀

def greenhorn(field): # юнга, рандом
    while True:
        x, y = [random.randint(0, 9), random.randint(0, 9)]

        if field[y][x] == 0:
            field[y][x] = 4
            break
        elif field[y][x] == 2:
            field[y][x] = 3
    return True

def harpooner(field): # гаупунер, охотник
    pass

def navigator(field): # штурман, шахматный
    pass

def admiral(field): # адмирал, тепловая карта
    pass

def master_seawolf(field): # мастер Морской волк, карта + история
    pass

# В играх сложность ботов обычно строится как «слоеный пирог»:
# каждый следующий уровень включает в себя фишки предыдущего.