import logging

from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import html, Router

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    logging.info(message.text)
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!\n\n"
                         f"Ro'yxatdan o'tish uchun  👉 /register kamandasini bosing")
