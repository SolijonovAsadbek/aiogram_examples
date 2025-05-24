import asyncio
import logging
import sys
from os import getenv

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
dp['start_datetime'] = datetime.now()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(Command('how_long_time_work'))
async def how_long_time_work(message: Message, start_datetime: datetime):
    delta_time = datetime.now() - start_datetime
    await message.answer(f'Bot {delta_time.seconds} sekundan beri ishlab turibdi!')


# formating HTML / Markdown-v2
@dp.message(Command('help'))
async def how_long_time_work(message: Message):
    fmt_text = ("<b>HMTL Formattig</b>\n\n"
                "Bold: <b>Salom</b>\n"
                "Italic: <i>Og'ma shiriftda yozish</i>\n"
                "youtube link: <a href=\"https://www.youtube.com/watch?v=DOkXgU-_cKU\">Video</a>\n"
                "Secret Key: <code>6563745419:AAHS4FI2A3B8fCEuO1svvWRM1adfiSNt-MM</code>")
    await message.answer(fmt_text)


async def start_up(bot: Bot):
    for admin in set(ADMINS):
        try:
            await bot.send_message(chat_id=admin, text='Bot ishga tushdi!')
        except Exception as e:
            print(f'{e}: {admin} id lik user aniqlanmadi!')


async def shut_down(bot: Bot):
    for admin in set(ADMINS):
        try:
            await bot.send_message(chat_id=admin, text='Bot o`chdi!')
        except Exception as e:
            print(f'{e}: {admin} id lik user aniqlanmadi!')


async def add_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Bot ishga tushdi!'),
        BotCommand(command='help', description='Yordam olish'),
        BotCommand(command='info', description='Mening ma`lumotlarim!'),
        BotCommand(command='how_long_time_work', description='Botni yoshi!')
    ]
    await bot.set_my_commands(commands=commands)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await add_commands(bot)
    # bot yonganda ishga tushadi
    dp.startup.register(start_up)
    # bot o'chganda ishga tushadi
    dp.shutdown.register(shut_down)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
