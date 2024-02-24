# -------------------------#
# ---Program by MiVainer---#
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.for_questions import get_yes_no_kb

router = Router()  # [1]

@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    text = '<b>Я бот для рассылки специальных предложений.</b>' #можно пользоваться тегами HTML, это мы указали в файле bot_test.py
    await message.answer(
        f"<span class='tg-spoiler'>Вы довольны своей работой?</span>\n{text}",
        reply_markup=get_yes_no_kb() #обращаемся к функции в файле for_questions.py выводящей кнопки в ответ на сообщение
    )

@router.message(Command("help")) # [3]
async def cmd_start(message: Message):
    await message.answer(
        "Бот для рассылки специальных предложений клиентам",
    )

@router.message(Command("code")) # [4]
async def handle_command_code(message: Message):
    text = "Абракадабра какая-то"
    await message.answer(text=text)





# реакции на ответы пользователя из [2]
@router.message(F.text.lower() == "да")
async def answer_yes(message: Message):
    await message.answer(
        "Это здорово!",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text.lower() == "нет")
async def answer_no(message: Message):
    await message.answer(
        "Жаль...",
        reply_markup=ReplyKeyboardRemove()
    )