from aiogram import Router, F, html
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot_registor.states.register import FormState

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
    birthday = message.text
    # filter
    await state.update_data(birthday=birthday)
    await message.answer('Telefon raqam: ')
    await state.set_state(FormState.phone_number)


@register_router.message(FormState.phone_number)
async def phone_handler(message: Message, state: FSMContext):
    phone_number = message.text
    # filter
    await state.update_data(phone=phone_number)
    await message.answer('Ish joyingizni lakatsiyasini ulashing: ')
    await state.set_state(FormState.work_address)


@register_router.message(FormState.work_address)
async def address_handler(message: Message, state: FSMContext):
    work_address = message.text
    # filter
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
    await message.answer(f'Ma`lumotlaringizni tasdiqlaysizmi?\n\n {user_data}')
    await state.set_state(FormState.confirm)


@register_router.message(FormState.confirm)
async def confirm_handler(message: Message, state: FSMContext):
    confirm = message.text

    if confirm.casefold() == 'ha':
        datas = await state.get_data()
        fullname = datas.get('fullname', 'N/A')
        birthday = datas.get('birthday', 'N/A')
        phone = datas.get('phone', 'N/A')
        location = datas.get('location', 'N/A')
        user_chat_id = message.from_user.id
        username = message.from_user.username
        # db.save()
        await message.answer('Botdan foydalanishga xush kelibsiz!')
        await state.clear()

    # Yoq: /register ga qaytaramiz!
    elif confirm.casefold() == 'yo`q':
        await message.answer('Qayta ro`yxatdan o`tish uchun  👉 /register kamandasini bosing')
        await state.clear()
    else:
        await message.reply('Ha yoki Yo`q bilan tasdiqlang iltimos!')
