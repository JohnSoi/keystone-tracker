from app.core.database import BaseRepository

from .model import Habit as HabitModel


class HabitRepository(BaseRepository[HabitModel]):
    _MODEL = HabitModel
