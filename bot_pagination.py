import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

# Bot token can be obtained via https://t.me/BotFather
load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()

smile_data = [('☹️', ' Hafa'), ('😐', 'Jiddiy'), ('🙂', 'Tabassum'), ('🤩', 'Baxtli')]


class PageCallbackData(CallbackData, prefix='page'):  # page:prev:2 page:next:2
    action: str
    page: int


def page_keyboard(page: int = 0):
    kbs = [
        [
            InlineKeyboardButton(
                text='⬅️ Avvalgi',
                callback_data=PageCallbackData(action='prev', page=page).pack()),

            InlineKeyboardButton(
                text='➡️ Keyingi',
                callback_data=PageCallbackData(action='next', page=page).pack())

        ]
    ]

    ikbs = InlineKeyboardMarkup(inline_keyboard=kbs)
    return ikbs


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
