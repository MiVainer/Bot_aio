# -------------------------#
# ---Program by MiVainer---#
import asyncio
import logging
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile, URLInputFile, BufferedInputFile
from aiogram import Bot, Dispatcher, types, F, html
from aiogram.filters.command import Command, CommandObject, CommandStart
from config_reader import config
from datetime import datetime
from aiogram.utils.formatting import Bold, as_list, as_marked_section, as_key_value, HashTag, Text

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")

# Создаём диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
'''@dp.message(Command("start"))
async def get_message(message: types.Message):
    await message.answer("Привет братишка! Как тебя зовут?")'''

# Если не указать фильтр F.text,
# то хэндлер сработает даже на картинку с подписью /test
@dp.message(F.text, Command("test"))
async def any_message(message: types.Message):
    await message.answer(
        "Hello, <u>world</u>!",
        parse_mode=ParseMode.HTML
    )

# Хендлер приветствия по полному имени
@dp.message(Command("hello"))
async def cmd_hello(message: types.Message):
    content = Text(
        "Hello, ",
        Bold(message.from_user.full_name)
    )
    await message.answer(
        **content.as_kwargs()
    )

# Отображение сложных конструкций
@dp.message(Command("example"))
async def cmd_advanced_example(message: types.Message):
    content = as_list(
        as_marked_section(
            Bold("Success:"),
            "Test 1",
            "Test 3",
            "Test 4",
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Failed:"),
            "Test 2",
            marker="❌ ",
        ),
        as_marked_section(
            Bold("Summary:"),
            as_key_value("Total", 4),
            as_key_value("Success", 3),
            as_key_value("Failed", 1),
            marker="  ",
        ),
        HashTag("#test"),
        sep="\n\n",
    )
    await message.answer(**content.as_kwargs())

# Получаем текст от пользователя и бот добавляет к нему время
#@dp.message(F.text)
#async def echo_with_time(message: types.Message):
    # Получаем текущее время в часовом поясе ПК
#    time_now = datetime.now().strftime('%H:%M')
    # Создаём подчёркнутый текст
#    added_text = html.underline(f"Создано в {time_now}")
    # Отправляем новое сообщение с добавленным текстом
#    await message.answer(f"{message.text}\n\n{added_text}", parse_mode="HTML")


# Работа с entities
# Telegram сильно упрощает жизнь разработчикам, выполняя предобработку сообщений
# пользователей на своей стороне. Например, некоторые сущности, типа e-mail, номера телефона,
# юзернейма и др. можно не доставать регулярными выражениями, а извлечь напрямую из объекта
# Message и поля entities, содержащего массив объектов типа MessageEntity.
# В качестве примера напишем хэндлер, который извлекает ссылку, e-mail и
# моноширинный текст из сообщения (по одной штуке).

"""@dp.message(F.text)
async def extract_data(message: types.Message):
    data = {
        "url": "<N/A>",
        "email": "<N/A>",
        "code": "<N/A>"
    }
    entities = message.entities or []
    for item in entities:
        if item.type in data.keys():
            # Неправильно
            # data[item.type] = message.text[item.offset : item.offset+item.length]
            # Правильно
            data[item.type] = item.extract_from(message.text)
    await message.reply(
        "Вот что я нашёл:\n"
        f"URL: {html.quote(data['url'])}\n"
        f"E-mail: {html.quote(data['email'])}\n"
        f"Пароль: {html.quote(data['code'])}"
    )
    """

# Команды и аргументы
@dp.message(Command("settimer"))
async def cmd_settimer(
        message: types.Message,
        command: CommandObject
):
    # Если не переданы никакие аргументы, то
    # command.args будет None
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return
    # Пробуем разделить аргументы на две части по первому встречному пробелу
    try:
        delay_time, text_to_send = command.args.split(" ", maxsplit=1)
    # Если получилось меньше двух частей, вылетит ValueError
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/settimer <time> <message>"
        )
        return
    await message.answer(
        "Таймер добавлен!\n"
        f"Время: {delay_time}\n"
        f"Текст: {text_to_send}"
    )


@dp.message(Command("help"))
@dp.message(CommandStart(
    deep_link=True, magic=F.args == "help"
))
async def cmd_start_help(message: Message):
    await message.answer("Это сообщение со справкой")

@dp.message(F.animation)
async def echo_gif(message: Message):
    await message.reply_animation(message.animation.file_id)


# Отправка фото
@dp.message(Command('images'))
async def upload_photo(message: Message):
    # Сюда будем помещать file_id отправленных файлов, чтобы потом ими воспользоваться
    file_ids = []

    # Отправка файла по ссылке
    image_from_url = URLInputFile("https://s1.1zoom.ru/big3/984/Canada_Parks_Lake_Mountains_Forests_Scenery_Rocky_567540_3840x2400.jpg")
    result = await message.answer_photo(
        image_from_url,
        caption="Изображение по ссылке"
    )
    file_ids.append(result.photo[-1].file_id)
    await message.answer("Отправленные файлы:\n"+"\n".join(file_ids))

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="С пюрешкой"),
            types.KeyboardButton(text="Без пюрешки")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ подачи"
    )
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)
# Ответ на нажатие кнопок
    @dp.message(F.text.lower() == "с пюрешкой")
    async def with_puree(message: types.Message):
        await message.reply("Отличный выбор!")

    @dp.message(F.text.lower() == "без пюрешки")
    async def without_puree(message: types.Message):
        await message.reply("Так невкусно!")


@dp.message(Command("reply_builder"))
async def reply_builder(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)
    await message.answer(
        "Выберите число:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
