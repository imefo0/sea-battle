import random

def greenhorn(field): # юнга, рандом
    return [random.randint(0, 9), random.randint(0, 9)]

def harpooner(): # гарпунер, охотник
    pass

def navigator(): # штурман, шахматный
    pass

def admiral(): # адмирал, тепловая карта
    pass

def master_seawolf(): # мастер Морской волк, карта + история
    pass

# В играх сложность ботов обычно строится как «слоеный пирог»:
# каждый следующий уровень включает в себя фишки предыдущего.