"""Модуль репозитория пользователя."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import hash_password
from app.core.database import BaseRepository

from .model import User as UserModel


class UserRepository(BaseRepository[UserModel]):
    """Репозиторий пользователя."""

    _MODEL = UserModel

    async def get_by_login(self, login: str) -> UserModel | None:
        """
        Получение пользователя по логину.

        Args:
            login (str): Логин пользователя.

        Returns:
            (UserModel | None): Данные пользователя. None, если пользователь не найден.

        Examples:
            >>> from fastapi import Depends
            >>> from app.core import BaseSchema
            >>> from app.core.database import get_db
            >>>
            >>> async def user_login(payload: BaseSchema, db: AsyncSession = Depends(get_db)) -> BaseSchema:
            ...     user: UserModel = await UserRepository().get_by_login(payload.login)
            ...     return BaseSchema(**user.to_dict()
        """
        user_data: UserModel | None = await self._session_db.scalar(select(UserModel).where(UserModel.login == login))

        if not user_data:
            return None

        return user_data

    async def get_by_email(self, email: str) -> UserModel | None:
        """
        Получение пользователя по email.

        Args:
            email (str): Email пользователя.

        Returns:
            (UserModel | None): Данные пользователя. None, если пользователь не найден.

        Examples:
            >>> from fastapi import Depends
            >>> from app.core import BaseSchema
            >>> from app.core.database import get_db
            >>>
            >>> async def user_login(payload: BaseSchema, db: AsyncSession = Depends(get_db)) -> BaseSchema:
            ...     user: UserModel = await UserRepository().get_by_email(payload.email)
            ...     return BaseSchema(**user.to_dict()
        """
        user_data: UserModel | None = await self._session_db.scalar(select(UserModel).where(UserModel.email == email))

        if not user_data:
            return None

        return user_data

    async def _before_create(self, data: dict) -> None:
        data["password"] = hash_password(str(data.get("password")))

    async def _before_update(self, _: UserModel, new_data: dict) -> None:
        if new_data.get("password"):
            new_data["password"] = hash_password(str(new_data.get("password")))
