from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    waiting_for_set_number = State()
    waiting_for_set_answer = State()