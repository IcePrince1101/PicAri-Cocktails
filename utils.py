# Взято из PicAri Bot - основного проекта из семейства
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def kb_generator(btns: list) -> InlineKeyboardMarkup:
    """
    Принимает на входе список с данными для кнопок,
    возвращает объект клавиатуры
    Пример списка
    [
        <Если одна кнопка>
        [Ряд],
        [
            <если в одном ряду несколько кнопок>
            [столбец 1] [столбец2]
            [столбец 1] [столбец2]
        ]
        [
            [
                <наполнение каждой кнопки>
                [<Текст кнопки>, <Callback-data кнопки>]
            ]
        ]
    ]
    params:
    - list - список с данными для кнопок
    return:
    - InlineKeyboardMarkup - объект клавиатуры
    """
    if len(btns) == 0:
        raise Exception("Клавиатура не может быть пустой")
    for i in range(len(btns)):
        for j in range(len(btns[i])):
            if len(btns[i][j]) != 2:
                raise Exception(
                    "Кнопка должна содержать текст и callback_data")
            btns[i][j] = InlineKeyboardButton(
                text=btns[i][j][0],
                callback_data=btns[i][j][1]
            )
    return InlineKeyboardMarkup(inline_keyboard=btns)