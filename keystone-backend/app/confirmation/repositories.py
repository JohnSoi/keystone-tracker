"""Модуль репозиториев для подтверждения."""

from app.core.database import BaseRepository

from .model import Confirmation as ConfirmationModel


class ConfirmationRepository(BaseRepository[ConfirmationModel]):
    """Репозиторий для подтверждения."""

    _MODEL = ConfirmationModel
