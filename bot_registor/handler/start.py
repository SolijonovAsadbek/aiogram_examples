import logging

from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import html, Router

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler1(message: Message) -> None:
    logging.info(message.text)
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
