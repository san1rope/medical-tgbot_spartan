from typing import Optional

from asyncpg import UniqueViolationError

from app.tg_bot.config import Config
from app.tg_bot.db_models.schemas import *


class DbQuestionSchema:
    def __init__(
            self, db_id: Optional[int] = None, tg_user_id: Optional[int] = None, question_text: Optional[str] = None,
            question_photo_files_id: Optional[str] = None, answer_text: Optional[str] = None,
            answer_photo_files_id: Optional[str] = None
    ):
        self.db_id = db_id
        self.tg_user_id = tg_user_id
        self.question_text = question_text
        self.question_photo_files_id = question_photo_files_id
        self.answer_text = answer_text
        self.answer_photo_files_id = answer_photo_files_id

    async def add(self) -> Union[Account, None, bool]:
        try:
            target = QuestionSchema(
                tg_user_id=self.tg_user_id, question_text=self.question_text,
                question_photo_files_id=self.question_photo_files_id, answer_text=self.answer_text,
                answer_photo_files_id=self.answer_photo_files_id
            )
            return await target.create()

        except UniqueViolationError as ex:
            Config.logger.error(ex)
            return False

    async def select(self) -> Union[QuestionSchema, List[QuestionSchema], None, bool]:
        try:
            q = QuestionSchema.query

            if self.db_id is not None:
                return await q.where(QuestionSchema.id == self.db_id).gino.first()

            if self.tg_user_id is not None:
                return await q.where(QuestionSchema.tg_user_id == self.tg_user_id).gino.all()

            return await q.gino.all()

        except Exception as ex:
            Config.logger.error(ex)
            return False

    async def update(self, **kwargs) -> Union[QuestionSchema, bool]:
        try:
            if not kwargs:
                return False

            target = await self.select()
            return await target.update(**kwargs).apply()

        except Exception as ex:
            Config.logger.error(ex)
            return False


class DbConsultants:
    def __init__(
            self, db_id: Optional[int] = None, tg_user_id: Optional[int] = None, full_name: Optional[str] = None
    ):
        self.db_id = db_id
        self.tg_user_id = tg_user_id
        self.full_name = full_name

    async def add(self) -> Union[Consultant, None, bool]:
        try:
            target = Consultant(tg_user_id=self.tg_user_id, full_name=self.full_name)
            return await target.create()

        except UniqueViolationError as ex:
            Config.logger.error(ex)
            return False

    async def select(self) -> Union[Consultant, List[Consultant], None, bool]:
        try:
            q = Consultant.query

            if self.db_id is not None:
                return await q.where(Consultant.id == self.db_id).gino.first()

            if self.tg_user_id is not None:
                return await q.where(Consultant.tg_user_id == self.tg_user_id).gino.all()

            return await q.gino.all()

        except Exception as ex:
            Config.logger.error(ex)
            return False

    async def update(self, **kwargs) -> Union[Consultant, bool]:
        try:
            if not kwargs:
                return False

            target = await self.select()
            return await target.update(**kwargs).apply()

        except Exception as ex:
            Config.logger.error(ex)
            return False
