import sys
import os
import subprocess
import main, bot
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
        # Вариант без пайпа (через shell)
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
    main.start(*result[7:])

def normal_start(result):
    main.start(*result[7:])

def help_cmd():
    print("флаг\tполная версия\tинформация\t\t\tзнач. по умолчанию")
    print("-"*75)
    print("-h\t--help\t\tотладка по командам\t\tFalse")
    print("-v\t--version\tверсия игры\t\t\tFalse")
    print("-f\t--fast\t\tбыстрый запуск\t\t\tFalse")
    print("\t\t\t(автоматически -c -r -s 1 -m")
    print("\t\t\t1111222334 -b harpooner -t")
    print("\t\t\tplayer, без задержки")
    print("\t\t\t(bot's turn...))")
    print("-c\t--clear\t\tочистить консоль перед игрой\tFalse")
    print("-r\t--random\tслучайные корабли\t\tFalse")
    print("-d\t--debug\t\tспециальная отладка для\t\tFalse")
    print("\t\t\tразработчиков")
    print("-l\t--language\tязык игры\t\t\ten")
    print("-t\t--turn\t\tпервый игрок\t\t\tplayer")
    print("-s\t--set-ship\tвид постановки корабля\t\t1")
    print("-b\t--bot\t\tзапустить бота\t\t\tharpooner")
    print("-m\t--method\tспособ постановки корабля\t1111222334")

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
    
    language = get_arg('-l', '--language', 'ru')
    turn = get_arg('-t', '--turn', 'player')
    set_ship = get_arg('-s', '--set-ship', '1')
    bot_name = get_arg('-b', '--bot', 'harpooner')
    method = get_arg('-m', '--method', '1111222334')
    
    return [help, version, fast, clear, random, debug, language, turn, set_ship, bot_name, method]

if __name__ == "__main__":
    result = parse()
    DEBUG = result[5] # --debug

    if result[3]: os.system("clear")

    if result[0] and result[1]: # --help --vesion
        help_cmd()
        version()
        exit(0)
    elif result[0]: help_cmd(); exit(0) # --help
    elif result[1]: version(); exit(0) # --version

    if result[4]: # --random
        print("random ship placement will be added after 1.0.0")

    if result[5]: # --debug
        debug.DEBUG = True

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
# -l    --language  язык игры                       en
# -t    --turn      первый игрок                    player
# -s    --set-ship  вид постановки корабля          1
# -b    --bot       запустить бота                  harpooner
# -m    --method    способ постановки корабля       1111222334