# -------------------------#
# ---Program by MiVainer---#
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from dataclasses import dataclass

from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_reader import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")

# Создаём диспетчер
dp = Dispatcher()


@dataclass
class Item:
    title: str
    description: str
    start_parameter: str
    currency: str
    prices: list[types.LabeledPrice]
    provider_data: dict = None
    photo_url: str = None
    photo_size: int = None
    photo_width: int = None
    photo_height: int = None
    need_name: bool = False
    need_phone_number: bool = False
    need_email: bool = False
    need_shipping_address: bool = False
    send_phone_number_to_provider: bool = False
    send_email_to_provider: bool = False
    is_flexible: bool = False
    provider_token: str = "1744374395:TEST:c78b93b33c07915cb286" # Тут не забудьте указать токен платежной системы, который выдает BotFather

    def generate_invoices(self):
        return self.__dict__


ACTION = Item(
    title='ACTION',
    description="Жанр компьютерных игр, в котором делается упор на эксплуатацию физических возможностей игрока.\nЖанр представлен во множестве разновидностей от файтингов, шутеров и до платформеров",
    currency='RUB',
    prices=[types.LabeledPrice(label="игры жанра Action:", amount=300000),
            types.LabeledPrice(label='Доставка', amount=15000),
            types.LabeledPrice(label='Скидка', amount=-20000)],
    start_parameter='create_invoice_lenovo_3',
    photo_url="https://portagame.ru/katalog/game/xbox-game/xboxone-just-cause-4_4.jpg",
    photo_size=350500,
    need_shipping_address=True,
    is_flexible=True
)

MMO = Item(
    title='MMO',
    description="Жанр компьютерных игр, основанный на элементах игрового процесса традиционных настольных ролевых игр.",
    currency='RUB',
    prices=[types.LabeledPrice(label="игры жанра MMO:", amount=190000),
            types.LabeledPrice(label='Доставка', amount=15000),
            types.LabeledPrice(label='Скидка', amount=-20000)],
    start_parameter='create_invoice_lenovo_3',
    photo_url="https://onyxgame.com/img/game/royal-quest/screenshots/royal-quest-image-screenshot-7.jpg",
    photo_size=535500,
    need_shipping_address=True,
    is_flexible=True
)

RGP = Item(
    title='RGP',
    description="Жанр компьютерных игр, основанный на элементах игрового процесса традиционных настольных ролевых игр.",
    currency='RUB',
    prices=[types.LabeledPrice(label="игры жанра RGP:", amount=230000),
            types.LabeledPrice(label='Доставка', amount=15000),
            types.LabeledPrice(label='Скидка', amount=-21000)],
    start_parameter='create_invoice_lenovo_3',
    photo_url="https://kingame.ru/wp-content/uploads/5/1/f/51f9c4452ad5c60225306c8d0cfafa67.jpeg",
    photo_size=2535500,
    need_shipping_address=True,
    is_flexible=True
)

POST_REGULAR_SHIPPING = types.ShippingOption(
    id='post_reg',
    title='Почтой',
    prices=[
        types.LabeledPrice(
            label='Обычная коробка',
            amount=0
        ),
        types.LabeledPrice(
            label='Почтой',
            amount=500_00
        ),
    ]
)

POST_FAST_SHIPPING = types.ShippingOption(
    id='post_fast',
    title='Почтой, ускоренная',
    prices=[
        types.LabeledPrice(
            label='Прочная упаковка',
            amount=200_00
        ),
        types.LabeledPrice(
            label='Срочной почтой',
            amount=1000_00
        ),
    ]
)

PICKUP_SHIPPING = types.ShippingOption(
    id='pickup',
    title='Самовывоз',
    prices=[
        types.LabeledPrice(
            label='Самовывоз из магазина',
            amount=100_00
        ),
    ]
)


@dp.message(Command('start'))
async def process_start_command(message: types.Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Action',
                                            callback_data='Action'
                                            ),
    InlineKeyboardButton(text='MMO',
                         callback_data='MMO'
                         ),
    InlineKeyboardButton(text='RPG',
                         callback_data='RPG')
                        )
    await message.answer('Здравствуйте!\nВы находитесь в магазине игр\nВыберите жанр игры:',
                         reply_markup=keyboard.as_markup()
                         )


@dp.callback_query(F.data == "Action")
async def show_invoices(message: types.Message):
    await bot.send_invoice(message.from_user.id, **ACTION.generate_invoices(), payload='12345')


@dp.callback_query(F.data == 'MMO')
async def show_invoices(callback: types.CallbackQuery):
    await bot.send_invoice('Добро пожаловать', **MMO.generate_invoices(), payload='12345')


@dp.callback_query(F.data == 'RPG')
async def show_invoices(callback: types.CallbackQuery):
    await bot.send_invoice('Добро пожаловать', **RGP.generate_invoices(), payload='12345')


@dp.shipping_query()
async def choose_shipping(query: types.ShippingQuery):
    if query.shipping_address.country_code == 'RU':
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[
                                            POST_REGULAR_SHIPPING,
                                            POST_FAST_SHIPPING,
                                            PICKUP_SHIPPING
                                        ],
                                        ok=True)
    elif query.shipping_address.country_code:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=False,
                                        error_message='Мы патриоты и работаем только по России\nВ выбранную вами страну товар не доставляемga')


@dp.pre_checkout_query()
async def process_pre_checkout_query(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)
    await bot.send_message(chat_id=query.from_user.id, text='Спасибо за покупку')


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot, skip_updates=False)

if __name__ == "__main__":
    asyncio.run(main())