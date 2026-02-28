import os
from logging import Logger
from pathlib import Path
from typing import Optional, Dict

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from pytz import timezone
from redis.asyncio import Redis


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN").strip()
    BOT = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    REDIS_IP: str = os.getenv("REDIS_IP").strip()
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD").strip()
    REDIS = Redis(
        host=REDIS_IP, port=6379, db=0, decode_responses=False, socket_keepalive=True,
        password=REDIS_PASSWORD, health_check_interval=15, socket_connect_timeout=5
    )
    DISPATCHER = Dispatcher(storage=RedisStorage(redis=REDIS))

    ADMINS = list(map(int, os.getenv("ADMINS").strip().split(",")))
    TIMEZONE = timezone(os.getenv("TIMEZONE").strip())

    logger: Optional[Logger] = None
    LOGGING_DIR = Path(os.path.abspath("logs"))
    DATETIME_FORMAT = "%d-%m-%Y_%H-%M-%S"

    DATABASE_CLEANUP = bool(int(os.getenv("DATABASE_CLEANUP")))
    DB_USER = os.getenv("DB_USER").strip()
    DB_PASSWORD = os.getenv("DB_PASSWORD").strip()
    DB_HOST = os.getenv("DB_HOST").strip()
    DB_NAME = os.getenv("DB_NAME").strip()

    KEYBOARD_BUTTONS: Dict = {}
