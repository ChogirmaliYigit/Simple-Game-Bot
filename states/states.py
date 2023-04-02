from aiogram.dispatcher.filters.state import State, StatesGroup


class GameState(StatesGroup):
    sender_user = State()
    results = State()
