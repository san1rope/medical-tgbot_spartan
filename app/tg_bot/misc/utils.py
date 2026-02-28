import json
import logging
import os
from pathlib import Path
from typing import Union, List, Optional
from datetime import datetime

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup

from app.tg_bot.config import Config


class Utils:

    @staticmethod
    async def send_step_message(state: FSMContext, text: str, markup: Optional[InlineKeyboardMarkup] = None):
        await Utils.delete_messages(state=state)
        msg = await Config.BOT.send_message(
            chat_id=state.key.user_id, text=text, reply_markup=markup, disable_web_page_preview=True)
        await Utils.add_msg_to_delete(state=state, msg_id=msg.message_id)

        return msg

    @staticmethod
    async def add_msg_to_delete(state: FSMContext, msg_id: Union[str, int]):
        try:
            temp_msg_ids: List = await state.get_value("temp_msg_ids")
            if temp_msg_ids is None:
                temp_msg_ids = []

            temp_msg_ids.append(msg_id)
            await state.update_data(temp_msg_ids=temp_msg_ids)

        except Exception as ex:
            Config.logger.error(f"Couldn't add msg_id to msg_to_delete\n{ex}")

    @staticmethod
    async def delete_messages(state: FSMContext):
        try:
            temp_msg_ids = await state.get_value("temp_msg_ids")
            if not temp_msg_ids:
                return

            for msg_id in temp_msg_ids:
                try:
                    await Config.BOT.delete_message(chat_id=state.key.user_id, message_id=msg_id)

                except TelegramBadRequest:
                    continue

            await state.update_data(temp_msg_ids=[])

        except KeyError:
            return

    @staticmethod
    async def add_logging(process_id: int, datetime_of_start: Union[datetime, str]) -> logging.Logger:
        if isinstance(datetime_of_start, str):
            file_dir = datetime_of_start

        elif isinstance(datetime_of_start, datetime):
            file_dir = datetime_of_start.strftime(Config.DATETIME_FORMAT)

        else:
            raise TypeError("datetime_of_start must be str or datetime")

        log_filepath = Path(os.path.abspath(f"{Config.LOGGING_DIR}/{file_dir}/{process_id}.txt"))
        log_filepath.parent.mkdir(parents=True, exist_ok=True)
        log_filepath.touch(exist_ok=True)

        logger = logging.getLogger()
        if logger.handlers:
            logger.handlers.clear()

        logger.setLevel(logging.INFO)
        logging.getLogger("aiogram.event").setLevel(logging.WARNING)
        logging.getLogger("gino").setLevel(logging.WARNING)
        formatter = logging.Formatter(u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - ' + str(
            process_id) + '| %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(log_filepath, mode="a", encoding="utf-8")
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    @staticmethod
    async def load_data():
        with open(os.path.abspath("app/tg_bot/misc/data/keyboard_buttons.json"), "r", encoding="utf-8") as file:
            Config.KEYBOARD_BUTTONS = json.load(file)
