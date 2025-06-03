import logging

from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import html, Router, F

from keyboard.inline.button import courses_ibtn
from utils.db.psql_db import User, session
from utils.db.psql_pscopg import get_by_id

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message):
    logging.info(message.text)
    chat_id = message.chat.id
    # if User.check_register(session, chat_id):
    if get_by_id(chat_id):
        return await message.answer(text='Botga xush kelibsiz!', reply_markup=courses_ibtn())
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!\n\n"
                         f"Ro'yxatdan o'tish uchun  👉 /register kamandasini bosing")


@start_router.callback_query()
async def courses_handler(call: CallbackQuery):
    match call.data:
        case 'py':
            # + logika
            await call.message.answer(f'Python programming language')
        case 'go':
            await call.message.answer(f'Go google')
        case 'c':
            await call.message.answer(f'C dasturlash tili')
        case 'c#':
            await call.message.answer(f'C# Micrasoft')
        case _:
            await call.message.answer(f'Tanimadim!')

