import asyncio
from datetime import datetime

from aiogram.types import BotCommand

from app.tg_bot.config import Config
from app.tg_bot.db_models.db_gino import connect_to_db
from app.tg_bot.handlers import routers
from app.tg_bot.misc.utils import Utils as Ut


async def main():
    datetime_of_start = datetime.now(tz=Config.TIMEZONE).strftime(Config.DATETIME_FORMAT)
    logger = await Ut.add_logging(datetime_of_start=datetime_of_start, process_id=0)
    Config.logger = logger

    await connect_to_db(remove_data=Config.DATABASE_CLEANUP)

    if routers:
        Config.DISPATCHER.include_routers(*routers)

    bot_commands = [
        BotCommand(command="start", description="Главное меню"),
        BotCommand(command="ask_question", description="Задать вопрос"),
        BotCommand(command="my_questions", description="Мои вопросы")
    ]
    await Config.BOT.set_my_commands(commands=bot_commands)

    await Config.BOT.delete_webhook(drop_pending_updates=True)
    await Config.DISPATCHER.start_polling(Config.BOT, allowed_updates=Config.DISPATCHER.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
