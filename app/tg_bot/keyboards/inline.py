from typing import Union

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.tg_bot.config import Config


class CustomCallback(CallbackData, prefix="cc"):
    role: str
    data: str


class InlineMarkups:

    GENERAL_MENU = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❔ Задать вопрос", callback_data="ask_question")
        ],
        [
            InlineKeyboardButton(text="❓ Мои вопросы", callback_data="my_questions")
        ],
        [
            InlineKeyboardButton(text="👨‍⚕️ Стать консультантом", callback_data="become_consultant")
        ]
    ])

    @staticmethod
    async def continents(cont_cd: str, back_cd: str, back_custom_cd: str = None) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(inline_keyboard=[])

        for el in Config.KEYBOARD_BUTTONS["continents"]:
            markup.inline_keyboard.append([])
            for cont_name, cont_data in el.items():
                markup.inline_keyboard[-1].append(InlineKeyboardButton(
                    text=cont_name, callback_data=CustomCallback(role=cont_cd, data=cont_data).pack()))

        markup.inline_keyboard.append(
            (await InlineMarkups.back(callback_data=back_cd, custom_callback_data=back_custom_cd)).inline_keyboard[0]
        )

        return markup

    @staticmethod
    async def countries(
            continent: str, page: int, count_cd: str, back_cd: str, back_custom_cd: str = None) \
            -> Union[InlineKeyboardMarkup, None]:
        markup = InlineKeyboardMarkup(inline_keyboard=[])

        key = f"countries_{continent}_{page}"
        if key not in Config.KEYBOARD_BUTTONS:
            return None

        for el in Config.KEYBOARD_BUTTONS[key]:
            markup.inline_keyboard.append([])
            for country_name, country_data in el.items():
                count_cd_tmp = count_cd
                if country_data.startswith("act:"):
                    count_cd_tmp = f"{count_cd}_{country_data.replace('act:', '')}"
                    country_data = ""
                    if ":" in count_cd_tmp:
                        country_data = count_cd_tmp[count_cd_tmp.index(":") + 1:]
                        count_cd_tmp = count_cd_tmp[:count_cd_tmp.index(":")]

                print(f"{count_cd_tmp}  :  {country_data}")
                markup.inline_keyboard[-1].append(InlineKeyboardButton(
                    text=country_name,
                    callback_data=CustomCallback(role=count_cd_tmp, data=country_data).pack()
                ))

        markup.inline_keyboard.append(
            (await InlineMarkups.back(callback_data=back_cd, custom_callback_data=back_custom_cd)).inline_keyboard[0]
        )

        return markup


    @staticmethod
    async def back(callback_data: str, custom_callback_data: str = None) -> InlineKeyboardMarkup:
        if custom_callback_data is not None:
            callback_data = CustomCallback(role=callback_data, data=custom_callback_data).pack()

        return InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="⬅️ Назад", callback_data=callback_data)
                ]
            ]
        )
