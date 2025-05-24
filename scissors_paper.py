import asyncio
import logging
import sys
from os import getenv
import random

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from datetime import datetime
from dotenv import load_dotenv

# Bot token can be obtained via https://t.me/BotFather
load_dotenv()
TOKEN = getenv("BOT_TOKEN")
ADMINS = getenv('ADMINS').split(',')  # '12488921,42149128'.split(',')

# [tosh, qaychi, qog'oz]

dp = Dispatcher()
dp['store'] = {
    "data": ['tosh', 'qaychi', 'qog`oz'],
    "bot": 0,
    "human": 0,
    'attempt': 1}


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!\n\n"
                         f"Tosh, Qaychi, Qog'oz o'yiniga xush kelibsiz\n\n"
                         f"<b>🎮 O'yin boshlandi!</b>")
    await message.answer('🤖 Bot: Tosh, qaychi, qog`oz?')


@dp.message()
async def game_mode(message: Message, store: dict):
    attempt = store.get('attempt')
    human = store.get('human')
    bot = store.get('bot')

    if attempt == 4:
        if human > bot:
            await message.answer("🎉 Odam yutdi!\nHissob: {}")
        return

    data = store.get('data')
    bot_said = random.choice(data)
    human_said = message.text.lower()

    await message.answer('')


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
