import sys
import os
import subprocess
import language as l
import debug

def get_latest_tag_master():
    try:
        return subprocess.check_output(
            ['git', 'describe', '--tags', '--abbrev=0', 'master'],
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"

def get_latest_tag_over_all_time():
    try:
        result = subprocess.check_output(
            "git tag --sort=-creatordate | head -1",
            shell=True,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
        return result if result else "unknown"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"

def main_menu(result):
    distance = 20
    status = ["no", "en", "player", "1 (for ex. A1 E1)", "1111222334", "harpooner"]
    while True:
        print("-"*distance, l.msg("Sea Battle"), "-"*distance)
        print("\t", l.msg("1) New Game"))
        print("\t", l.msg("2) Settings"))
        print("\t", l.msg("3) Quit"))

        print()
        print(l.msg("Select an Item"))

        while True:
            choice = input("> ")
            if choice not in ["1", "2", "3"]:
                print(l.msg("Incorrect input"))
            else:
                break

        if choice == "1":
            normal_start(result)
        elif choice == "2":
            while True:
                print("-"*distance, "Settings", "-"*distance)
                print(f"\tSetting\t\t\t\tStatus")
                print(f"\t1) Start Game\t\t\tYES")
                print(f"\t2) Random Placement Ships\t{status[0]}")
                print(f"\t3) Game Language\t\t{status[1]}")
                print(f"\t4) 1st Player\t\t\t{status[2]}")
                print(f"\t5) Ship Placement Type\t\t{status[3]}")
                print(f"\t6) Method to Place Ships\t{status[4]}")
                print(f"\t7) Bot Name\t\t\t{status[5]}")
                print(f"\t8) Exit\t\t\t\tNO")

                print("Which option do you want to change?")
                while True:
                    choice = input("> ")
                    if choice not in list(map(str, range(1, 9))):
                        print("Incorrect input")
                    else:
                        break

                if choice == "1":
                    #   0       1       2     3       4      5        6      7       8         9        10     11
                    # [help, version, fast, clear, random, debug, language, turn, set_ship, bot_name, method, menu]
                    result[4] = False if status[0] == "no" else True # random
                    result[6] = status[1]
                    result[7] = status[2]
                    result[8] = status[3][0]
                    result[9] = status[5]
                    result[10] = status[4]
                    normal_start(result)
                    status = ["no", "en", "player", "1 (for ex. A1 JI)", "1111222334", "harpooner"]
                    break
                elif choice == "2":
                    while True:
                        choice = input("What do you want to exchange it for? [yes/no] ")
                        if choice not in ["no", "yes"]:
                            print("Incorrect input")
                        else: 
                            break
                    status[0] = choice
                elif choice == "3":
                    while True:
                        choice = input("What do you want to exchange it for? [ru/en] ")
                        if choice not in ["ru", "en"]:
                            print("Incorrect input")
                        else: 
                            break
                    status[1] = choice
                elif choice == "4":
                    while True:
                        choice = input("What do you want to exchange it for? [player/bot] ")
                        if choice not in ["player", "bot"]:
                            print("Incorrect input")
                        else: 
                            break
                    status[2] = choice
                elif choice == "5":
                    while True:
                        choice = input("What do you want to exchange it for? [1/2] (1: A1 E1, 2: A1 > 5 / A1 r 5) ")
                        if choice == "1":
                            status[3] = choice + " (for ex. A1 E1)"
                            break
                        elif choice == "2":
                            status[3] = choice + " (for ex. A1 >/r 5)"
                            break
                        else:
                            print("Incorrect input")
                elif choice == "6":
                    while True:
                        choice = input("What do you want to exchange it for? ")
                        if not choice.isdigit():
                            print("Incorrect input")
                        else: 
                            break
                    status[4] = choice
                elif choice == "7":
                    while True:
                        choice = input("What do you want to exchange it for? [greenhorn/harpooner/navigator/admiral/master_seawolf] ")
                        if choice not in ["greenhorn", "harpooner", "navigator", "admiral", "master_seawolf"]:
                            print("Incorrect input")
                        else: 
                            break
                    status[5] = choice
                elif choice == "8":
                    print("Exit")
                    break
            
        else:
            print("Quit")
            break

def fast_start(result):
    __import__('main').start(*result[7:-1])

def normal_start(result):
    __import__('main').start(*result[7:-1])

def help_cmd():
    print(l.msg(f"Using: python3 start.py [-c] [-d] [-f] [-r] [-b BOT] [-t TURN] [-s MODE] [-m METHOD] [-l LANG]"))
    print()
    print(f"{l.msg("flag")}{l.msg("full version")}{l.msg("info")}{l.msg("default value")}")
    print(f"-"*75)
    print(f"-h\t--help\t\t{l.msg("help with commands")}False")
    print(f"-v\t--version\t{l.msg("game version")}False")
    print(f"-f\t--fast\t\t{l.msg("fast start")}False")
    print(f"\t\t\t{l.msg("(automatic set -c -r -s 1 -m 1111222334 -b harpooner -t player)")}")
    print(f"-c\t--clear\t\t{l.msg("clear console before the game")}False")
    print(f"-r\t--random\t{l.msg("random placement ships")}False")
    print(f"-d\t--debug\t\t{l.msg("special debug for developers")}")
    print(f"-l\t--language\t{l.msg("game language [ru/en]")}en")
    print(f"-t\t--turn\t\t{l.msg("1st player")}player")
    print(f"-s\t--set-ship\t{l.msg("ship placement type")}1")
    print(f"-b\t--bot\t\t{l.msg("type of bot")}harpooner")
    print(f"-m\t--method\t{l.msg("method to place ships")}1111222334")

def version():
    print(f"Sea Battle\tActual: {get_latest_tag_master()}\n\t\tNewest: {get_latest_tag_over_all_time()}")

def flag_in_cmd(short_flag, long_flag, cmd) -> bool:
    return short_flag in cmd or long_flag in cmd

def parse():
    c = sys.argv[1:]
    
    # Флаги без аргументов
    help = '-h' in c or '--help' in c
    version = '-v' in c or '--version' in c
    fast = '-f' in c or '--fast' in c
    clear = '-c' in c or '--clear' in c
    random = '-r' in c or '--random' in c
    debug = '-d' in c or '--debug' in c
    
    # Флаги с аргументами
    def get_arg(short, long, default):
        for i, arg in enumerate(c):
            if arg == short or arg == long:
                if i + 1 < len(c):
                    return c[i + 1]
                return default
        return default
    
    language = get_arg('-l', '--language', 'en')
    turn = get_arg('-t', '--turn', 'player')
    set_ship = get_arg('-s', '--set-ship', '1')
    bot_name = get_arg('-b', '--bot', 'harpooner')
    method = get_arg('-m', '--method', '1111222334')

    menu = not any([help, version, fast, random, debug, flag_in_cmd("-t", "--turn", c),
                    flag_in_cmd("-s", "--set-ship", c), flag_in_cmd("-b", "--bot", c),
                    flag_in_cmd("-m", "--method", c)])

    return [help, version, fast, clear, random, debug, language, turn, set_ship, bot_name, method, menu]

if __name__ == "__main__":
    result = parse()

    if result[-1]: # menu
        main_menu(result)
    else:
        debug.DEBUG = result[5] # --debug
        l.LANGUAGE = result[6] # --language
        # print(result)

        if result[3]: os.system("clear")

        if result[0] and result[1]: # --help --vesion
            help_cmd()
            version()
            exit(0)
        elif result[0]: help_cmd(); exit(0) # --help
        elif result[1]: version(); exit(0) # --version

        if result[4]: # --random
            print("random ship placement will be added after 1.0.0")

        if result[2]: # --fast
            fast_start(result)
        else:
            normal_start(result)


# config    -                               изменение дефолтное значение
# config default                            дефолтные настройки конфига
# config imefo.flags.set-ship --default     сбросить метод set-ship у дефолтных значений у пользователя imefo
# config user.flags.debug true             изменить у пользователя user флаг debug на true всегда
# -------------------------------------------------------------
# -h    --help      отладка по командам             False
# -v    --version   версия игры                     False
# -f    --fast      быстрый запуск                  False
#                   (автоматически -c -r -s 1 -m
#                   1111222334 -b harpooner -t
#                   player, без задержки
#                   (bot's turn...))
# -c    --clear     очистить консоль перед игрой    False
# -r    --random    случайные корабли               False
# -d    --debug     специальная отладка для         False
#                   разработчиков                   
# -l    --language  язык игры [ru/en]               en
# -t    --turn      первый игрок                    player
# -s    --set-ship  вид постановки корабля          1
# -b    --bot       запустить бота                  harpooner
# -m    --method    способ постановки корабля       1111222334
# -M    --menu      включить главное меню для       False 
#                   настроек