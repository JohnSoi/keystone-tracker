"""Пакет для работы с пользователями."""

from .model import User as UserModel
from .routes import user_routes
from .dependencies import get_current_user
