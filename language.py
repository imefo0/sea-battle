LANGUAGE = "en"

TEXTS = {
    "ru": {
        "player's turn to place ships": "ход игрока чтобы поставить корабли",
        "incorrect input": "неверный ввод",
        "incorrect set-ship value": "верное значенине для set-ship",
        "bot's turn to place ships": "ход бота чтобы поставить корабли",
        "player's turn": "ход игрока",
        "bot's turn": "ход бота",
        "master_seawolf doesn't work now": "мастер морской волк пока не работает",
        "incorrect bot name": "неверное название бота",
        "incorrect turn": "неверное название хода",
        "error": "ошибка",
        "player won": "игрок выиграл",
        "bot won": "бот выиграл",

        "Using: python3 start.py [-c] [-d] [-f] [-r] [-b BOT] [-t TURN] [-s MODE] [-m METHOD] [-l LANG]":
            "Использование: python3 start.py [-c] [-d] [-f] [-r] [-b БОТ] [-t ХОД] [-s РЕЖИМ] [-m МЕТОД] [-l ЯЗЫК]",
        "flag": "флаг\t",
        "full version": "полная версия\t",
        "info": "информация\t\t\t",
        "default value": "знач. по умолчанию",
        "help with commands": "помощь по командам\t\t",
        "game version": "версия игры\t\t\t",
        "fast start": "быстрый запуск\t\t\t",
        "(automatic set -c -r -s 1 -m 1111222334 -b harpooner -t player)": "(автоматически -c -r -s 1 -m\n\t\t\t1111222334 -b harpooner -t\n\t\t\tplayer)",
        "clear console before the game": "очистить консоль перед игрой\t",
        "random placement ships": "рандомная постанока кораблей\t",
        "special debug for developers": "специальная отладка для\t\tFalse\n\t\t\tразработчиков",
        "game language [ru/en]": "язык игры [ру/англ]\t\t",
        "1st player": "1-ый игрок\t\t\t",
        "ship placement type": "вид постановки кораблей\t\t",
        "type of bot": "тип бота\t\t\t",
        "method to place ships": "способ постановки кораблей\t"
    },
    "en": {
        "player's turn to place ships": "player's turn to place ships",
        "incorrect input": "incorrect input",
        "incorrect set-ship value": "incorrect set-ship value",
        "bot's turn to place ships": "bot's turn to place ships",
        "player's turn": "player's turn",
        "bot's turn": "bot's turn",
        "master_seawolf doesn't work now": "master seawolf doesn't work now",
        "incorrect bot name": "incorrect bot name",
        "incorrect turn": "incorrect turn",
        "error": "error",
        "player won": "player won",
        "bot won": "bot won", 

        "Using: python3 start.py [-c] [-d] [-f] [-r] [-b BOT] [-t TURN] [-s MODE] [-m METHOD] [-l LANG]":
            "Using: python3 start.py [-c] [-d] [-f] [-r] [-b BOT] [-t TURN] [-s MODE] [-m METHOD] [-l LANG]",
        "flag": "flag\t",
        "full version": "full version\t",
        "info": "info\t\t\t\t",
        "default value": "default value",
        "help with commands": "help with commands\t\t",
        "game version": "game version\t\t\t",
        "fast start": "fast start\t\t\t",
        "(automatic set -c -r -s 1 -m 1111222334 -b harpooner -t player)": "(automatic set -c -r -s 1 -m\n\t\t\t1111222334 -b harpooner -t\n\t\t\tplayer)",
        "clear console before the game": "clear console before the game\t",
        "random placement ships": "random placement ships\t\t",
        "special debug for developers": "special debug for developers\tFalse",
        "game language [ru/en]": "game language [ru/en]\t\t",
        "1st player": "1st player\t\t\t",
        "ship placement type": "ships placement type\t\t",
        "type of bot": "type of bot\t\t\t",
        "method to place ships": "method to place ships\t\t"
    }
}

def msg(key: str) -> str:
    return TEXTS[LANGUAGE].get(key, key)