"""Пакет для работы с базой данных."""

from .db_manager import DatabaseManager, database_manager
from .dependencies import get_db
from .mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin
from .model import BaseModel
