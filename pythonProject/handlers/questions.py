# -------------------------#
# ---Program by MiVainer---#
import emoji
import re
import aiofiles
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile, InputFile, BufferedInputFile
from aiogram.utils import markdown
from aiogram.enums import ChatAction
import csv
import json



from keyboards.for_questions import get_yes_no_kb

router = Router()  # [1]

@router.message(F.from_user.id.in_({457820697, 680365312}), Command("start", prefix="!/%"))  # [2] ответ на команду /start, только от меня и Сани
async def cmd_start(message: Message):
    text = f"<b>Привет {message.from_user.full_name}! Я бот для рассылки специальных предложений.</b>" #можно пользоваться тегами HTML, это мы указали в файле bot_test.py
    url = "https://static21.tgcnt.ru/posts/_0/06/06bdace22a1652e8f154b114d403a260.jpg"
    await message.answer(
        f"{markdown.hide_link(url)}{text}\nНачинаем создание рассылки?", # вставил картинку, а затем спойлер
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

@router.message(F.from_user.id.in_({457820697, 680365312}), Command("help", prefix="!/%")) # [3] ответ на команду /help
async def cmd_start(message: Message):
    await message.answer(
        "Бот для рассылки специальных предложений клиентам",
    )


@router.message(F.from_user.id.in_({457820697, 680365312}), Command("base", prefix="!/%")) # загрузить базу абонентов
async def cmd_base(message: Message):
    text = f"{message.from_user.full_name}, закидывай мне базу в формате <b>csv</b> братишка!😉" #можно пользоваться тегами HTML, это мы указали в файле bot_test.py
    await message.answer(
        text = text
    )
# отправка определённого файла со стороны бота (test.txt), например выслать имеющуюся загруженную базу
@router.message(Command("file"))
async def handle_command_file(message: Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        # action=ChatAction.TYPING,
        # action=ChatAction.UPLOAD_PHOTO,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    file_path = "/home/mihail/Bot_aio/pythonProject/baza/test.txt"
    await message.reply_document(
        document=FSInputFile(
            path=file_path,
            filename="test.txt",
        ),
    )

# скачивание файла в определённую дирректорию /baza, и парсинг базы
@router.message(F.document)
async def handle_document(message: Message):
    if message.document.mime_type == 'text/csv':
        file_id = message.document.file_id
        file_path = f"/home/mihail/Bot_aio/pythonProject/baza/testbd.csv"  # Путь для сохранения файла
        file_obj = await message.bot.download(file_id)
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_obj.read())

            await message.bot.send_chat_action(
                chat_id=message.chat.id,
                action=ChatAction.UPLOAD_DOCUMENT,
            )

            await message.answer(text='Загрузка базы завершена, бро!🫡 Начинаю проверку...🤯')

            # Преобразование строки из json в словарь python
            with open("/home/mihail/Bot_aio/pythonProject/baza/post.json", "r", encoding="utf-8") as f:
                post_json = f.read()
                f.close()
            post = json.loads(post_json)
            a = (post["pack"])

            # Наполнение словаря данными из csv базы
            with open("/home/mihail/Bot_aio/pythonProject/baza/testbd.csv", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=';')
                k = 0
                for row in reader:
                    k += 1
                    stre = re.sub('[^0-9]', '', row['Phone'])
                    a.append({"phone": f"{stre}",
                              "message": "Сударь, это тестовая рассылка",
                              "link": "https://ермак.shop/"})

            baza = post

            # красивая запись в json
            with open("/home/mihail/Bot_aio/pythonProject/baza/baza.json", "w", encoding="utf-8") as f:
                for chunk in json.JSONEncoder(ensure_ascii=False, indent=4).iterencode(baza):
                    f.write(chunk)

            await message.answer(
                text=f"Всего в базе {k} записей, на рассылку тебе потребуется примерно <b>{k * 5}</b> деревянных🫣")





'''    file_id = message.document.file_id
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    downloaded_file = await message.bot.download_file(file_path)

    with open(f"/home/mihail/Bot_aio/pythonProject/baza/testbd.csv", "wb") as file:
        file.write(downloaded_file.read())
'''





    #file_name = message.document.file_name
    #my_file = open(file_name, 'w+')
    #my_file.close()

@router.message(F.from_user.id.in_({457820697, 680365312})) # [4] ответ на команду /code
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



