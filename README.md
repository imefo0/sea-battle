[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)

# Sea Battle

## License

CLI game "Sea Battle" with AI bots
Copyright (C) 2026  imefo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

## About

Морской бой это игра где главная цель - убить все корабли. Есть всего 6 видов ботов:
1. **Юнга** - это бот, который стреляет в случайные клетки, даже при попадании стреляет случайно. Самый легкий бот.

2. **Гарпунер** - это усовершенствованный бот, который стреляет в случайные клетки, но при попадании начинает добивать корабль. Самый оптимальный бот для игр.

3. **Штурман** - это бот, который имеет шаблон клеток для выстрела, также добивает корабль. Чуть сложнее гарнунера.

4. **Адмирал** - это почти самый сильный бот, так как стреляет по тепловой карте (карта вероятностей, где выбирает самую "горячую" клетку для выстрела). Очень сильный бот.

5. *Злой Адмирал* - это лучшая версия адмирала, где стреляет также по тепловой карте, но добивает корабль. Самый лучший бот для "жарких" игр (пока не добавлен в игру).

6. **Мастер Морской Волк** - это самый сильный бот, когда либо. Вначале игр бот похож на адмирала, но после ~5-10 игр, он чувствует характер игрока и стреляет в самую горячую клетку и на клетку, где чаще всего ставил игрок. Самый сложный бот.

## Fast installing

> git clone https://github.com/imefo0/sea-battle.git
> cd sea-battle
> python3 start.py

Требование: **python 3.12+**

## Fast start

Чтобы быстро запустить морской бой следует выполнить команду:

> python3 start.py

Достаточно иметь **python3** и встроенные библиотеки **python3**

## Additional commands

Можно запустить игру через разные команды

> python3 start.py [`-c`] [`-d`] [`-f`] [`-r`] [`-b БОТ`] [`-t ХОД`] [`-s РЕЖИМ`] [`-m МЕТОД`] [`-l ЯЗЫК`]

```
**-h** --help: справка по командам
**-v** --version: показать версию игры
**-f** --fast: быстрый старт (автоматически -c -r -s 1 -m 1111222334 -b harpooner -t player)
**-c** --clear: очищать консоль перед игрой
**-r** --random: случайная постановка кораблей (пока недоступно)
**-d** --debug: специальная отладка
**-l** --language: язык игры [русский/английский]
**-t** --turn: первый игрок
**-s** --set-ship: тип постановки корабля [1/2] (1 - это A1 Д1, а 2 - A1 > 5)
**-b** --bot: тип бота
**-m** --method: метод расстановки (цифра - это кол-во палуб, а кол-во самих цифр - кол-во таких кораблей, например 1111222334 - 4 однопалубных, 3 двухпалубных, 2 трехпалубных и 1 четырехпалубный)
**-u** --user: выбрать пользователя для игры (если -1, играть без выбранного пользователя)
**-n** --new-user: создать пользователя, но заходить в игру как -1 (надо написать -n test -u test)
**-R** --remove-user: удалить пользователя, но заходить в игру как -1 
*-e* --emoji: вид поля из эмоджи (Пока не добавлен)
*-C* --cli: вид поля из ASCII символов (Пока не добавлен)
```

> **Примечание:** Флаги `-e` и `-C` находятся в разработке.

# Example of playing field

```
    A  B  C  D  E  F  G  H  I  J            A  B  C  D  E  F  G  H  I  J
 1 🌊 🌊 🌊 🔹 ❌️ 🔹 🌊 🌊 🌊 🌊         1 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊
 2 🌊 🚢 🚢 🔹 🔹 🔹 💥 💥 🚢 🌊         2 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊
 3 🔹 🌊 🌊 🌊 🌊 🌊 🌊 🔹 🌊 🌊         3 🌊 🌊 🌊 🔹 🌊 🌊 🔹 🌊 🌊 🌊
 4 🚢 🌊 🔹 🚢 🌊 🌊 🌊 🌊 🌊 🌊         4 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊
 5 🚢 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🔹 🚢         5 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊
 6 🚢 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🚢         6 🔹 🌊 🌊 🔹 🔹 🔹 🔹 🔹 🌊 🌊
 7 🚢 🌊 🌊 🌊 🌊 🌊 🌊 🚢 🌊 🌊         7 🌊 🌊 🌊 🔹 ❌️ ❌️ ❌️ 🔹 🌊 🌊
 8 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊         8 🌊 🌊 🌊 🔹 🔹 🔹 🔹 🔹 🌊 🌊
 9 🌊 🚢 🌊 🚢 🚢 🌊 🌊 🌊 🌊 🌊         9 🌊 🔹 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊
10 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🚢 🚢 🚢        10 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊 🌊
```