from sqlalchemy import Column, sql, BigInteger, Text, String

from app.tg_bot.db_models.db_gino import TimedBaseModel

prefix = "medical_tgbot_"


class QuestionSchema(TimedBaseModel):
    __tablename__ = prefix + "questions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tg_user_id = Column(BigInteger, nullable=False)
    question_text = Column(Text, nullable=False)
    question_photo_files_id = Column(String)
    answer_text = Column(Text, nullable=False)
    answer_photo_files_id = Column(String)

    query: sql.Select