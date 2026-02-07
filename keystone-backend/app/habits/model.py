from datetime import time, date

from sqlalchemy import String, Text, ForeignKey, Integer, Time, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM, ARRAY, JSON

from app.core.database import BaseModel
from .consts import DEFAULT_COLOR, FrequencyType, WeekDay


class Habit(BaseModel):
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    icon: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[str] = mapped_column(String(7), nullable=False, default=DEFAULT_COLOR)

    frequency_type: Mapped[str] = mapped_column(ENUM(FrequencyType), nullable=False, default=FrequencyType.DAILY)
    times_per_period: Mapped[int] = mapped_column(Integer, default=1)

    # Для weekly: массив дней недели [1,2,3,4,5,6,7]
    days_of_week: Mapped[list[int]] = mapped_column(
        ARRAY(Integer),
        default=[
            WeekDay.MONDAY,
            WeekDay.TUESDAY,
            WeekDay.WEDNESDAY,
            WeekDay.THURSDAY,
            WeekDay.FRIDAY,
            WeekDay.SATURDAY,
            WeekDay.SUNDAY,
        ],
    )

    preferred_times: Mapped[list[time]] = mapped_column(ARRAY(Time), nullable=True)

    # Цели
    target_streak: Mapped[int] = mapped_column(Integer, nullable=True)  # целевая цепочка
    target_count: Mapped[int] = mapped_column(Integer, nullable=True)  # целевое количество выполнений
    target_date: Mapped[date] = mapped_column(Date, nullable=True)  # дата цели

    # Категория
    category: Mapped[str] = mapped_column(String(100), nullable=True)

    # Статус
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

    # Даты
    start_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)

    # Статистика (вычисляемые поля)
    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0)
    total_completions: Mapped[int] = mapped_column(Integer, default=0)
    success_rate: Mapped[int] = mapped_column(Integer, default=0)  # процент успеха (0-100)

    # Настройки
    allow_partial: Mapped[bool] = mapped_column(Boolean, default=False)  # разрешить частичное выполнение
    require_notes: Mapped[bool] = mapped_column(Boolean, default=False)  # требовать заметки при отметке
    require_mood: Mapped[bool] = mapped_column(Boolean, default=False)  # требовать оценку настроения

    # Метаданные
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=[])
    custom_data: Mapped[dict] = mapped_column(JSON, nullable=True)  # для расширений

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
