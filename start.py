# CLI game "Sea Battle" with AI bots
# Copyright (C) 2026  imefo

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import os
import subprocess
import language as l
import debug
import user

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
    #         random lang   turn  set_ship  method      bot
    status = ["no", result[6], "player", "1", "1111222334", "harpooner", -1]
    while True:
        print("-"*distance, l.msg("Sea Battle"), get_latest_tag_master(), "-"*distance)
        print(f"\t1) {l.msg("New Game")}")
        print(f"\t2) {l.msg("Settings")}")
        print(f"\t3) {l.msg("Quit")}")

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
                print("-"*distance, f"{l.msg("Settings")}", "-"*distance)
                print(f"\t{l.msg("Setting")}\t\t\t\t{l.msg("Status")}")
                print(f"\t1) {l.msg("Start Game")}\t\t\t{l.msg("YES")}")
                print(f"\t2) {l.msg("Random Placement Ships")}\t{l.msg(status[0])}")
                print(f"\t3) {l.msg("Game Language")}\t\t{l.msg(status[1])}")
                print(f"\t4) {l.msg("1st Player")}\t\t\t{l.msg(status[2])}")
                print(f"\t5) {l.msg("Ship Placement Type")}\t\t{status[3]} ({l.msg("for ex.")} {"A1 E1" if status[3] == "1" else "A1 > 5"})")
                print(f"\t6) {l.msg("Method to Place Ships")}\t{l.msg(status[4])}")
                print(f"\t7) {l.msg("Bot Name")}\t\t\t{l.msg(status[5])}")
                print(f"\t8) {l.msg("User Name")}\t\t\t{l.msg(status[6])} {"(" if status[6] == -1 else ""}{l.msg("without user" if status[6] == -1 else "")}" + 
                      f"{")" if status[6] == -1 else ""}")
                print(f"\t9) {l.msg("Exit")}\t\t\t\t{l.msg("NO")}")

                print(l.msg("Which option do you want to change?"))
                while True:
                    choice = input("> ")
                    if choice not in list(map(str, range(1, 9))):
                        print("Incorrect input")
                    else:
                        break

                if choice == "1":
                    #   0       1       2     3       4      5        6      7       8         9        10     11    12
                    # [help, version, fast, clear, random, debug, language, turn, set_ship, bot_name, method, name, menu]
                    result[4] = False if status[0] == "no" else True # random
                    result[6] = status[1]
                    result[7] = status[2]
                    result[8] = status[3]
                    result[9] = status[5]
                    result[10] = status[4]
                    result[11] = status[6]
                    normal_start(result)
                    status = ["no", "en", "player", "1 (for ex. A1 EI)", "1111222334", "harpooner", -1]
                    break
                elif choice == "2":
                    while True:
                        choice = input(f"{l.msg("What do you want to exchange it for?")} [{l.msg("yes")}/{l.msg("no")}] ")
                        if choice not in ["no", "yes", "да", "нет"]:
                            print(l.msg("Incorrect input"))
                        else: 
                            break
                    status[0] = ["no", "yes"][["нет", "да"].index(choice)] if choice not in ["no", "yes"] else choice
                elif choice == "3":
                    while True:
                        choice = input(f"{l.msg("What do you want to exchange it for?")} [{l.msg("ru")}/{l.msg("en")}] ")
                        if choice not in ["ru", "en", "ру", "англ"]:
                            print(l.msg("Incorrect input"))
                        else: 
                            break
                    status[1] = ["ru", "en"][["русс", "англ"].index(choice)] if choice not in ["ru", "en"] else choice
                    l.LANGUAGE = choice
                elif choice == "4":
                    while True:
                        choice = input(f"{l.msg("What do you want to exchange it for?")} [{l.msg("player")}/{l.msg("bot")}] ")
                        if choice not in ["player", "bot", "игрок", "бот"]:
                            print(l.msg("Incorrect input"))
                        else: 
                            break
                    status[2] = ["player", "bot"][["игрок", "бот"].index(choice)] if choice not in ["player", "bot"] else choice
                elif choice == "5":
                    while True:
                        choice = input(f"{l.msg("What do you want to exchange it for?")} [1/2] (1: A1 E1, 2: A1 > 5) ")
                        if choice == "1":
                            status[3] = choice
                            break
                        elif choice == "2":
                            status[3] = choice
                            break
                        else:
                            print(l.msg("Incorrect input"))
                elif choice == "6":
                    while True:
                        choice = input(f"{l.msg("What do you want to exchange it for?")} ")
                        if not choice.isdigit():
                            print(l.msg("Incorrect input"))
                        else: 
                            break
                    status[4] = choice
                elif choice == "7":
                    while True:
                        choice = input(f"{l.msg("What do you want to exchange it for?")} " +
                                       f"[{l.msg("greenhorn")}/{l.msg("harpooner")}/{l.msg("navigator")}/{l.msg("admiral")}/{l.msg("master_seawolf")}] ")
                        if choice not in ["greenhorn", "harpooner", "navigator", "admiral", "master_seawolf",
                                          "юнга", "гарпунер", "штурман", "адмирал", "мастер_морской_волк"]:
                            print(l.msg("Incorrect input"))
                        else: 
                            break
                    status[5] = ["greenhorn", "harpooner", "navigator", "admiral",
                                 "master_seawolf"][["юнга", "гарпунер", "штурман", "адмирал",
                                                    "мастер_морской_волк"].index(choice)] if choice not in ["greenhorn",
                                                                                                            "harpooner", "navigator",
                                                                                                            "admiral", "master_seawolf"] else choice
                elif choice == "8":
                    while True:
                        choice = input(f"{l.msg("What do you want to exchange it for?")} [-1/...] ")
                        if choice == "-1":
                            status[6] = int(choice)
                            break
                        else:
                            status[6] = choice
                            break
                elif choice == "9":
                    print(l.msg("Exit"))
                    break
            
        else:
            print(l.msg("Quit"))
            break

def fast_start(result):
    __import__('main').start(*result[7:-3])

def normal_start(result):
    __import__('main').start(*result[7:-3])

def help_cmd():
    print(l.msg(f"Using: python3 start.py [-c] [-d] [-f] [-r] [-b BOT] [-t TURN] [-s MODE] [-m METHOD] [-l LANG]"))
    print()
    print(f"{l.msg("flag")}{l.msg("full version")}{l.msg("info")}{l.msg("default value")}")
    print(f"-"*75)
    print(f"-h\t--help\t\t{l.msg("help with commands")}{l.msg("False")}")
    print(f"-v\t--version\t{l.msg("game version")}{l.msg("False")}")
    print(f"-f\t--fast\t\t{l.msg("fast start")}{l.msg("False")}")
    print(f"\t\t\t{l.msg("(automatic set -c -r -s 1 -m 1111222334 -b harpooner -t player)")}")
    print(f"-c\t--clear\t\t{l.msg("clear console before the game")}{l.msg("False")}")
    print(f"-r\t--random\t{l.msg("random placement ships")}{l.msg("False")}")
    print(f"-d\t--debug\t\t{l.msg("special debug for developers")}")
    print(f"-l\t--language\t{l.msg("game language [ru/en]")}en")
    print(f"-t\t--turn\t\t{l.msg("1st player")}player")
    print(f"-s\t--set-ship\t{l.msg("ship placement type")}1")
    print(f"-b\t--bot\t\t{l.msg("type of bot")}harpooner")
    print(f"-m\t--method\t{l.msg("method to place ships")}1111222334")
    print(f"-u\t--user\t\t{l.msg("select user to play")}-1 ({l.msg("without user")})")
    print(f"-n\t--new-user\t{l.msg("create user")}\t\t{l.msg("False")}")
    print(f"-R\t--remove-user\t{l.msg("removing user")}\t\t\t{l.msg("False")}")

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
    name = get_arg('-u', '--user', -1)
    new = get_arg('-n', '--new-user', -1)
    remove = get_arg('-R', '--remove-user', -1)

    menu = not any([help, version, fast, random, debug, flag_in_cmd("-t", "--turn", c),
                    flag_in_cmd("-s", "--set-ship", c), flag_in_cmd("-b", "--bot", c),
                    flag_in_cmd("-m", "--method", c), flag_in_cmd("-u", "--user", c), 
                    flag_in_cmd("-n", "--new-user", c), flag_in_cmd("-R", "--remove-user", c)])

    return [help, version, fast, clear, random, debug, language, turn, set_ship, bot_name, method, name, new, remove, menu]

if __name__ == "__main__":
    result = parse()

    l.LANGUAGE = result[6] # --language
    if result[3]: os.system("clear") # --clear

    if result[-1]: # menu
        main_menu(result)
    else:
        debug.DEBUG = result[5] # --debug
        # print(result)


        if result[0] and result[1]: # --help --vesion
            help_cmd()
            version()
            exit(0)
        elif result[0]: help_cmd(); exit(0) # --help
        elif result[1]: version(); exit(0) # --version

        if result[13] != -1: # --remove-user
            user.remove_user(result[13])

        if result[12] != -1: # --new-user
            user.add_user(result[12])

        if not user.exist_user(result[11]) and result[11] != -1: # --user
            print(f"user {result[11]} does not exist")

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