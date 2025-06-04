import asyncio
import logging
import sys
from enum import Enum, Flag
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv

# Bot token can be obtained via https://t.me/BotFather
load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()

smile_data = [('☹️', 'Hafa'), ('😐', 'Jiddiy'), ('🙂', 'Tabassum'), ('🤩', 'Baxtli')]


class Action(Enum):
    PREVIOUS = 'prev'
    NEXT = 'next'


class PageCallbackData(CallbackData, prefix='page'):  # page:prev:2 page:next:2
    action: str
    page: int


def page_keyboard(page: int = 0):
    kbs = [
        [
            InlineKeyboardButton(
                text=f'⬅️{page - 1}',
                callback_data=PageCallbackData(action=Action.PREVIOUS.value, page=page).pack()),

            InlineKeyboardButton(
                text=f'{page}', callback_data=f'{page}'),

            InlineKeyboardButton(
                text=f'{page + 1}➡️',
                callback_data=PageCallbackData(action=Action.NEXT.value, page=page).pack())
        ]
    ]

    rkbs = kbs.pop(0)

    if page == 0:
        rkbs.pop(0)
    elif page == len(smile_data) - 1:
        rkbs.pop()

    kbs.append(rkbs)

    ikbs = InlineKeyboardMarkup(inline_keyboard=kbs)
    return ikbs


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!\n"
                         f"Sahifalash uchun /page kamadasini yozing!")


@dp.message(Command('page'))
async def page_handler(message: Message):
    await message.answer(f"{smile_data[0][0]}", reply_markup=page_keyboard())


@dp.callback_query(PageCallbackData.filter())
async def callback_query_page_handler(call: CallbackQuery, callback_data: PageCallbackData):
    page = callback_data.page
    action = callback_data.action

    if 0 <= page < len(smile_data) and action == Action.NEXT.value:
        page += 1
    elif page > 0 and action == Action.PREVIOUS.value:
        page -= 1

    smile_text = smile_data[page][0]  # + ' - ' + smile_data[page][1]

    if smile_text != call.message.text:
        await call.message.edit_text(smile_text, reply_markup=page_keyboard(page))

        await call.answer(cache_time=1)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
