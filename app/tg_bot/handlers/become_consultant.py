from typing import Union

from aiogram import Router, F, types, enums
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.tg_bot.config import Config

router = Router()


@router.message(F.chat.type == enums.ChatType.PRIVATE, Command("become_consultant"))
@router.callback_query(F.data == "become_consultant")
async def cmd_become_consultant(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    uid = message.from_user.id
    Config.logger.info(f"Handler called. {cmd_become_consultant.__name__}. user_id={uid}")

    if isinstance(message, types.CallbackQuery):
        await message.answer()

    text = [
        "<b>👨‍⚕️ Стать консультантом</b>",
        "\n<b></b>"
    ]
