from enum import StrEnum, IntEnum


class FrequencyType(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


class WeekDay(IntEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


DEFAULT_COLOR: str = "#3B82F6"
COLOR_REGEX: str = r"^[0-9A-Fa-f]{6}$"
COLOR_START_WITH: str = "#"

DAYS_IN_WEEK: int = 7
