from datetime import time, date

from pydantic import BaseModel, Field, field_validator

from .consts import DEFAULT_COLOR, FrequencyType, WeekDay
from .exceptions import StartDateNoFutureException, EndDateBeforeStartDateException, EndDateNoPastException, \
    InvalidDayInWeekException, TooManyDaysOfWeekException
from .validators import validate_hex_color, validate_days_of_week


class MainHabitData(BaseModel):
    title: str = Field(..., min_length=2, max_length=255, description="Название привычки")
    description: str | None = Field(None, max_length=1000, description="Описание привычки")
    icon: str = Field(..., min_length=1, max_length=50, description="Иконка привычки")
    color: str | None = Field(DEFAULT_COLOR, min_length=7, max_length=7, description="Цвет привычки")
    category: str | None = Field(None, min_length=1, max_length=100, description="Категория привычки")

    @field_validator("color")
    @classmethod
    def validate_color(cls, value: str) -> str:
        return validate_hex_color(value)

class AdditionalHabitData(BaseModel):
    is_active: bool = Field(True, description="Активна ли привычка")
    is_archived: bool = Field(False, description="Архивирована ли привычка")
    start_date: date = Field(date.today(), description="Дата начала привычки")
    end_date: date | None = Field(None, description="Дата окончания привычки")
    tags: list[str] = Field(default_factory=list, description="Теги привычки")

    @field_validator("start_date")
    @classmethod
    def validate_start_date(cls, value: date) -> date:
        if value > date.today():
            raise StartDateNoFutureException()

        return value


    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, value: date | None, values: dict) -> date | None:
        if value is not None:
            if value < values["start_date"]:
                raise EndDateBeforeStartDateException()
            if value <= date.today():
                raise EndDateNoPastException()

        return value

class FrequencyHabitData(BaseModel):
    frequency_type: FrequencyType = Field(FrequencyType.DAILY, description="Тип частоты выполнения")
    times_per_period: int | None = Field(1, ge=1, description="Количество раз в период")
    days_of_week: list[int] | None = Field(default_factory=list, description="Дни недели выполнения")
    preferred_times: list[time] = Field(default_factory=list, description="Предпочтительные времена выполнения")

    @field_validator("days_of_week")
    @classmethod
    def validate_days_of_week(cls, value: list[int]) -> list[int]:
        return validate_days_of_week(value)


class TargetHabitData(BaseModel):
    target_streak: int | None = Field(None, ge=1, description="Целевое количество подряд идущих выполнений")
    target_count: int | None = Field(None, ge=1, description="Целевое количество выполнений")
    target_date: date | None = Field(None, description="Целевая дата")


class StreakHabitData(BaseModel):
    current_streak: int = Field(0, description="Текущий количество подряд идущих выполнений")
    longest_streak: int = Field(0, description="Самый большое количество подряд идущих выполнений")
    total_completions: int = Field(0, description="Общее количество выполнений привычки")
    success_rate: int = Field(0, lt=100, description="Процент успешных выполнений привычки")


class ServiceHabitData(BaseModel):
    user_id: int
    custom_data: dict | None = Field(None, description="Дополнительные данные для расширения")


class SettingsHabitData(BaseModel):
    allow_partial: bool = Field(False, description="Разрешить частичное выполнение")
    require_notes: bool = Field(False, description="Требовать заметки при отметке")
    require_mood: bool = Field(False, description="Требовать оценку настроения")

