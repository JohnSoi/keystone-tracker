"""Модуль репозитория пользователя."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core import hash_password
from .model import User as UserModel


class UserRepository:
    """
    Репозиторий пользователя.

    Attributes:
        _session_db (AsyncSession): Сессия базы данных.
    """

    def __init__(self, session_db: AsyncSession) -> None:
        """
        Инициализация репозитория пользователя.

        Args:
            session_db (AsyncSession): Сессия базы данных.
        """
        self._session_db: AsyncSession = session_db

    async def create(self, data: dict) -> dict:
        """
        Создание пользователя.

        Args:
            data (dict): Данные пользователя.

        Returns:
            (dict): Данные пользователя после создания.
        """
        model: UserModel = UserModel()

        data["password"] = hash_password(str(data.get("password")))

        for key, value in data.items():
            if hasattr(model, key):
                setattr(model, key, value)

        self._session_db.add(model)
        await self._session_db.commit()
        await self._session_db.refresh(model)

        return model.to_dict() or {}

    async def get_by_login(self, login: str) -> dict | None:
        """
        Получение пользователя по логину.

        Args:
            login (str): Логин пользователя.

        Returns:
            (dict | None): Данные пользователя. None, если пользователь не найден.

        Examples:
            >>> from fastapi import Depends
            >>> from app.core import BaseSchema
            >>> from app.database import get_db
            >>>
            >>> async def user_login(payload: BaseSchema, db: AsyncSession = Depends(get_db)) -> BaseSchema:
            ...     user: dict = await UserRepository().get_by_login(payload.login)
            ...     return BaseSchema(**user)
        """
        user_data: UserModel | None = await self._session_db.scalar(select(UserModel).where(UserModel.login == login))

        if not user_data:
            return None

        return user_data.to_dict() or {}

    async def get_by_email(self, email: str) -> dict | None:
        """
        Получение пользователя по email.

        Args:
            email (str): Email пользователя.

        Returns:
            (dict | None): Данные пользователя. None, если пользователь не найден.

        Examples:
            >>> from fastapi import Depends
            >>> from app.core import BaseSchema
            >>> from app.database import get_db
            >>>
            >>> async def user_login(payload: BaseSchema, db: AsyncSession = Depends(get_db)) -> BaseSchema:
            ...     user: dict = await UserRepository().get_by_email(payload.email)
            ...     return BaseSchema(**user)
        """
        user_data: UserModel | None = await self._session_db.scalar(select(UserModel).where(UserModel.email == email))

        if not user_data:
            return None

        return user_data.to_dict() or {}
