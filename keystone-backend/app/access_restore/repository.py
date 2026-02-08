"""Модуль репозитория для работы с токенами доступа."""

from app.core.database import BaseRepository

from .model import AccessRestore as AccessRestoreModel


class AccessRestoreRepository(BaseRepository[AccessRestoreModel]):
    """Репозиторий для работы с токенами доступа."""

    _MODEL = AccessRestoreModel
