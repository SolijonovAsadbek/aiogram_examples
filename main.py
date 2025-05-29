import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv

# Bot token can be obtained via https://t.me/BotFather
load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    print(123)


@dp.message(Command('getMe'))
async def get_me(message: Message):
    # variable
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    username = message.from_user.username

    # txt_forma
    text = (f"Salom, {first_name}\n"
            f"Chat ID: {chat_id}\n"
            f"Username: {username}")

    # xabar yuborish
    await message.answer(text)


@dp.message(F.text.in_({'aiogram', 'python', 'dotenv'}))
async def send_msg(message: Message):
    await message.reply('Python aiogram=3.0.0.b python-dotenv')


@dp.message(F.photo)  # F.document, F.contact, F.location, F.sticker, F.audio, F.poll, F.voice, F.text.regexp()
async def send_msg(message: Message):
    await message.reply('Rasm qabul qilindi!')


@dp.message(F.text.regexp(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+'))
async def email_handler(message: Message):
    email = message.text
    await message.reply(f'Bu email: {email}!')


@dp.message(F.text.regexp(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'))
async def text_contact_handler(message: Message):
    phone = message.text
    await message.reply(f'Bu telefon raqam: {phone}!')


@dp.message(
    F.text.regexp(
        r'^(19[0-9]{2}|20[0-1][0-9]|202[0-5])-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01]) ([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$'))
async def datetime_handler(message: Message):
    await message.answer(f'Datetime: {message.text} qabul qilindi!')


# @dp.message()
# async def echo_handler(message: Message) -> None:
#     try:
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         await message.answer("Nice try!")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
