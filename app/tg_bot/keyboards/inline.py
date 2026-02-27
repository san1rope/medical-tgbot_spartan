from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineMarkups:

    GENERAL_MENU = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Задать вопрос", callback_data="ask_question")
        ],
        [
            InlineKeyboardButton(text="Мои вопросы", callback_data="my_questions")
        ]
    ])
