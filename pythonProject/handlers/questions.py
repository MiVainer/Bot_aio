# -------------------------#
# ---Program by MiVainer---#
import emoji
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile, InputFile
from aiogram.utils import markdown
from aiogram import filters # использование конкретных user id


from keyboards.for_questions import get_yes_no_kb

router = Router()  # [1]

@router.message(F.from_user.id.in_({457820697, 680365312}), Command("start", prefix="!/%"))  # [2] ответ на команду /start, только от меня и Сани
async def cmd_start(message: Message):
    text = f"<b>Привет {message.from_user.full_name}! Я бот для рассылки специальных предложений.</b>" #можно пользоваться тегами HTML, это мы указали в файле bot_test.py
    url = "https://static21.tgcnt.ru/posts/_0/06/06bdace22a1652e8f154b114d403a260.jpg"
    await message.answer(
        f"{markdown.hide_link(url)}<span class='tg-spoiler'>{text}</span>\nНачинаем создание рассылки?", # вставил картинку, а затем спойлер
        reply_markup=get_yes_no_kb() #обращаемся к функции в файле for_questions.py выводящей кнопки в ответ на сообщение
    )

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

@router.message(Command("help", prefix="!/%")) # [3] ответ на команду /help
async def cmd_start(message: Message):
    await message.answer(
        "Бот для рассылки специальных предложений клиентам",
    )

@router.message()

@router.message() # [4] ответ на команду /code
async def handle_command_code(message: Message):
    text = emoji.emojize(f"Абракадабра какая-то, я тебя не понимаю 😰")

    await message.answer(text=text)


'''@router.message() # [5] эхо ответ
async def echo_message(message: Message):
    await message.answer( # просьба подождать
            text=f"<i>Сударь, прошу вас обождать пока я справлюсь по вашему вопросу...</i>",
    )
    try:
        #await message.copy_to(chat_id=message.chat.id) # пересылает сообщение (при добавлении опций можно переслать другому пользователю)
        await message.forward(chat_id=message.chat.id) # forward показывает от кого переслано сообщение
    except TypeError:
        await message.reply(text="Something new 🙂")'''



