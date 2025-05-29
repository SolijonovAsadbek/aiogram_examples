from aiogram.fsm.state import StatesGroup, State


class FormState(StatesGroup):
    fullname = State()
    birthday = State()
    phone_number = State()
    work_address = State()
    confirm = State()
