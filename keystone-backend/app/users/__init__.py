"""Пакет для работы с пользователями."""

from .dependencies import get_current_user
from .model import User as UserModel
from .routes import user_routes
