"""Пакет базового функционала приложения."""

from .model import BaseModel, UUIDMixin, TimestampMixin, SoftDeleteMixin
from .db_manager import DatabaseManager, database_manager, get_db
