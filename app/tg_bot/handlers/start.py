from typing import Union

from aiogram import Router, F, types, enums
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from app.tg_bot.config import Config
from app.tg_bot.keyboards.inline import InlineMarkups as Im
from app.tg_bot.misc.utils import Utils as Ut

router = Router()


@router.message(F.chat.type == enums.ChatType.PRIVATE, CommandStart())
async def cmd_start(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    uid = message.from_user.id
    Config.logger.info(f"Handler called. {cmd_start.__name__}. user_id={uid}")

    if isinstance(message, types.CallbackQuery):
        await message.answer()

    text = [
        "<b>Заголовок</b>",
        "\n<b>Описание для бота...</b>",
        "\n<b>Используйте клавиатуру под сообщением либо команды</b>"
    ]
    await Ut.send_step_message(state=state, text="\n".join(text), markup=Im.GENERAL_MENU)
