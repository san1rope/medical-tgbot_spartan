from aiogram.fsm.state import StatesGroup, State


class ConsultantRegistration(StatesGroup):
    Name = State()
    AboutYourself = State()
    Country = State()
    Locality = State()
    Email = State()
