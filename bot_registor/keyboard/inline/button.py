from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, SwitchInlineQueryChosenChat


def courses_ibtn():  # static
    kbs = [
        [
            InlineKeyboardButton(text='Python', callback_data='py'),
            InlineKeyboardButton(text='Go', callback_data='go')
        ],
        [
            InlineKeyboardButton(text='C', callback_data='c')
        ],
        [
            InlineKeyboardButton(text='C#', callback_data='c#'),
            InlineKeyboardButton(text='Admin', url='https://t.me/@careerpy'),
            InlineKeyboardButton(text='Wirte',
                                 switch_inline_query_current_chat='ib'),
            InlineKeyboardButton(text='Wirte2',
                                 switch_inline_query='')
        ]
    ]

    ikbs = InlineKeyboardMarkup(inline_keyboard=kbs)

    return ikbs
