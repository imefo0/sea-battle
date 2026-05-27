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

def fast_start(result):
    __import__('main').start(*result[7:])

def normal_start(result):
    __import__('main').start(*result[7:])

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
    
    return [help, version, fast, clear, random, debug, language, turn, set_ship, bot_name, method]

if __name__ == "__main__":
    result = parse()
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