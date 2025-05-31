import re
from datetime import datetime

from aiogram import Router, F, html
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from keyboard.default.button import share_location, confirm_button
from states.register import FormState
from utils.db.psql_db import User, session

register_router = Router()


@register_router.message(Command('register'))
async def register_start(message: Message, state: FSMContext):
    await message.answer('To`liq ismingiz: ')
    # 1-qadam
    await state.set_state(FormState.fullname)


@register_router.message(FormState.fullname)
async def fullname_handler(message: Message, state: FSMContext):
    fullname = message.text
    # filter
    await state.update_data(fullname=fullname)
    await message.answer('Tug`ilgan kuningiz: \n'
                         'Format: yyyy-mm-dd\n'
                         'Masalan: 2000-12-31')
    await state.set_state(FormState.birthday)


@register_router.message(FormState.birthday)
async def birthday_handler(message: Message, state: FSMContext):
    from keyboard.default.button import share_contact
    birthday = message.text
    pattern = r'^(?:(?:19[0-9]{2}|20[0-1][0-9]|202[0-4])-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12][0-9]|3[01])|(?:0[469]|11)-(?:0[1-9]|[12][0-9]|30)|02-(?:0[1-9]|1[0-9]|2[0-8])))|(?:(?:19(?:[02468][048]|[13579][26])|20(?:[02468][048]|[13579][26])|2000|2400)-02-29)$'
    if not re.match(pattern, birthday):
        return await message.answer('To`g`ri ma`lumot joylang!')
    # filter
    await state.update_data(birthday=birthday)
    await message.answer('Telefon raqam: ', reply_markup=share_contact())
    await state.set_state(FormState.phone_number)


@register_router.message(FormState.phone_number)
async def phone_handler(message: Message, state: FSMContext):
    phone_number = message.text
    if message.contact:
        phone_number = message.contact.phone_number
    # filter
    await state.update_data(phone=phone_number)
    await message.answer('Ish joyingizni lakatsiyasini ulashing: ', reply_markup=share_location())
    await state.set_state(FormState.work_address)


@register_router.message(FormState.work_address)
async def address_handler(message: Message, state: FSMContext):
    work_address = message.text
    if message.location:
        work_address = message.location.latitude, message.location.longitude
    await state.update_data(location=work_address)
    datas = await state.get_data()
    fullname = datas.get('fullname', 'N/A')
    birthday = datas.get('birthday', 'N/A')
    phone = datas.get('phone', 'N/A')
    location = datas.get('location', 'N/A')
    user_chat_id = message.from_user.id
    username = message.from_user.username
    user_data = (f"To'liq ism: {html.bold(fullname)}\n"
                 f"Tug'ilgan kun: {html.bold(birthday)}\n"
                 f"Telefon: {html.bold(phone)}\n"
                 f"Ish joyi: {html.bold(location)}\n"
                 f"Chat ID: {html.bold(user_chat_id)}\n"
                 f"Username: @{html.bold(username)}")
    await message.answer(f'Ma`lumotlaringizni tasdiqlaysizmi?\n\n{user_data}', reply_markup=confirm_button())
    await state.set_state(FormState.confirm)


@register_router.message(FormState.confirm)
async def confirm_handler(message: Message, state: FSMContext):
    confirm = message.text

    if confirm.casefold() == 'ha':
        datas = await state.get_data()
        fullname = datas.get('fullname')
        birthday = datetime.strptime(datas.get('birthday'), '%Y-%m-%d')
        phone = datas.get('phone')
        location = datas.get('location')
        user_chat_id = message.from_user.id
        username = message.from_user.username

        # database saqlashga tayyorlash
        user = User(fullname=fullname, birthday=birthday, phone=phone,
                    address=location, username=username, chat_id=user_chat_id)
        user.save(session=session)

        await message.answer('Botdan foydalanishga xush kelibsiz!', reply_markup=ReplyKeyboardRemove())
        await state.clear()

    # Yoq: /register ga qaytaramiz!
    elif confirm.casefold() == 'yo`q':
        await message.answer('Qayta ro`yxatdan o`tish uchun  👉 /register kamandasini bosing',
                             reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.reply('Ha yoki Yo`q bilan tasdiqlang iltimos!')
