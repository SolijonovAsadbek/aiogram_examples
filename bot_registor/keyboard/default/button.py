from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def share_contact():
    keyboards = [
        [
            KeyboardButton(text='Telefon ulashish1', request_contact=True),
            KeyboardButton(text='Telefon ulashish2', request_contact=True)
        ],
        [
            KeyboardButton(text='Telefon ulashish3', request_contact=True)
        ],
        [
            KeyboardButton(text='4', request_contact=True),
            KeyboardButton(text='5', request_contact=True),
            KeyboardButton(text='6', request_contact=True)
        ],
    ]
    kb = ReplyKeyboardMarkup(keyboard=keyboards,
                             resize_keyboard=True,
                             input_field_placeholder='Tugamadan foydalaning!')
    return kb


def share_location():
    keyboards = [

        [
            KeyboardButton(text='Manzilni ulasish', request_location=True)
        ],

    ]
    kb = ReplyKeyboardMarkup(keyboard=keyboards,
                             resize_keyboard=True,
                             input_field_placeholder='Tugamadan foydalaning!')
    return kb


def confirm_button():
    keyboards = [

        [
            KeyboardButton(text='Ha'),
            KeyboardButton(text='Yo`q')
        ],

    ]
    kb = ReplyKeyboardMarkup(keyboard=keyboards,
                             resize_keyboard=True,
                             input_field_placeholder='Tugamadan foydalaning!')
    return kb
