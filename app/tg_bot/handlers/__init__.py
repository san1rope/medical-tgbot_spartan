from .start import router as r_start
from .ask_question import router as r_ask_question
from .my_questions import router as r_my_questions
from .become_consultant import router as r_become_consultant

routers = [
    r_start,
    r_ask_question,
    r_my_questions,
    r_become_consultant
]
