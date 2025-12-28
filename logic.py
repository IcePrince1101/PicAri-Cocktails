import random

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, FSInputFile

from utils import kb_generator

from pprint import pprint

from data import *

router = Router()

@router.message(Command("start"))
async def start(
    message: Message,
):
    await message.answer(
        "Привет! Я бот, который сегодня выдаст тебе случайный рецепт коктейля."
        "Твоя задача - по выданной карточке приготовить коктейль, а другие могут оценить его "
        "и поставить свою оценку.\n\nДля получения карточки введите команду /get_cocktail\n"
        "Можно посмотреть оценку по своим коктейлям командой /view_score\n"
        "Можно посмотреть топ по оценкам командой /view_top_score"
    )

@router.message(Command("reset"))
async def reset(
    message: Message
):
    SCORE.clear()
    await message.answer("Список коктейлей сброшен!")

@router.message(Command("get_cocktail"))
async def get_cocktail(
    message: Message,
    bot: Bot,
):
    all = list(NAMINGS.keys())
    used = list(SCORE.keys())
    available = list(set(all) - set(used))
    if available == []:
        await message.answer("Список коктейлей закончился! Можете перезапустить бота командой /reset")
        return
    image = random.choice(available)

    await message.answer(f"@{message.from_user.username}, твой коктейль:")
    await message.answer(HISTORY[image])

    SCORE[image] = {}
    SCORE[image]["author"] = {}
    SCORE[image]["author"]["username"] = message.from_user.username
    SCORE[image]["author"]["name"] = message.from_user.first_name
    SCORE[image]["score"] = {}
    kb = [[]]
    for i in range(1, 6):
        kb[0].append(
            [
                f"{i}",
                f"score:{image}:{i}"
            ]
        )
    kb += [
        [
            [
                f"Убрать оценку",
                f"remove_score:{image}"
            ]
        ]
    ]
    image = FSInputFile("cards/" + image)
    await message.answer_photo(image, has_spoiler=True, reply_markup=kb_generator(kb))

@router.callback_query(F.data.startswith("score:"))
async def score(
    callback: CallbackQuery
):
    image, score = callback.data.split(":")[1:]
    if callback.from_user.username == SCORE[image]["author"]["username"]:
        await callback.message.answer(
            f"Хе-хе, @{callback.from_user.username}! Ты не можешь поставить оценку самому себе!"
        )
        return
    data = {}
    data["name"] = callback.from_user.first_name
    data["value"] = score
    SCORE[image]["score"][callback.from_user.username] = data
    await callback.message.answer(
        f"@{callback.from_user.username} поставил оценку {score} для коктейля {NAMINGS[image]}, "
        f"который готовил {SCORE[image]['author']['name']} @{SCORE[image]['author']['username']}")

@router.callback_query(F.data.startswith("remove_score:"))
async def remove_score(
    callback: CallbackQuery
):
    image = callback.data.split(":")[1]
    SCORE[image]["score"].pop(callback.from_user.username)
    await callback.message.answer(f"@{callback.from_user.username} убрал свою оценку")

@router.message(Command("view_score"))
async def next(
    message: Message
):
    answer = str()
    begin_message = f"@{message.from_user.username}, твои коктейли и их оценки:\n"
    for key, value in SCORE.items():
        values = []
        if value["author"]["username"] == message.from_user.username:
            answer += f"{NAMINGS[key]}\n"
            for key2, value2 in value["score"].items():
                answer += f"\t\t\t\t{key2}: {value2['value']}\n"
                values.append(int(value2["value"]))
            if len(values) != 0:
                answer += f"\t\tСредняя оценка: {sum(values) / len(values)}\n\n"
            else:
                answer += "\t\tЕще никто не оценил этот коктейль\n\n"
    if answer == "":
        answer = f"@{message.from_user.username}, у тебя нет коктейлей, которые ты готовил"
    else:
        answer = begin_message + answer
    await message.answer(answer)

@router.message(Command("view_top_score"))
async def view_top_score(
    message: Message
):
    score = {}
    for key, value in SCORE.items():
        score[key] = {}
        score[key]["author"] = value["author"]
        values = SCORE[key]["score"]
        count = 0
        sum = 0
        for key2, value2 in values.items():
            sum += int(values[key2]["value"])
            count += 1
        count = 1 if count == 0 else count
        score[key]["score"] = sum / count
    
    sorted_score = dict(sorted(score.items(), key=lambda x: x[1]["score"], reverse=True))
    top = str()
    place = 1
    for key, value in sorted_score.items():
        top += f"{place}) {NAMINGS[key]} ({value['author']['name']} @{value['author']['username']}) -- {value['score']}\n"
        place += 1
    answer = f"@{message.from_user.username}, топ по оценкам:\n"
    answer += top
    await message.answer(answer)