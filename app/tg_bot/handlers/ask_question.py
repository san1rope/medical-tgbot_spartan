from typing import Union

from aiogram import Router, F, types, enums
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.tg_bot.config import Config

router = Router()


@router.message(F.chat.type == enums.ChatType.PRIVATE, Command("ask_question"))
@router.callback_query(F.data == "ask_question")
async def cmd_ask_question(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    uid = message.from_user.id
    Config.logger.info(f"Handler caled. {cmd_ask_question.__name__}. user_id={uid}")

    if isinstance(message, types.CallbackQuery):
        await message.answer()

    text = [
        "<b>❔ Задать вопрос</b>",
        "\n<b>Перед вопросом, вам нужно выбрать консультанта, который будет рассматривать ваш вопрос</b>"
    ]
