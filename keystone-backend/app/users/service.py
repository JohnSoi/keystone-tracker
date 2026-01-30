"""Модуль сервиса для работы с пользователями."""

from sqlalchemy.ext.asyncio import AsyncSession

from ..core import create_access_token, verify_password
from .exceptions import (
    EmailConflictException,
    LoginConflictException,
    LoginNotFoundException,
    PasswordIncorrectException,
)
from .repository import UserRepository
from .schemas import UserAccessData, UserAuthResponseData, UserRegisterData


class UserService:
    """
    Сервис для работы с пользователями.

    Attributes:
        _repository (UserRepository): Репозиторий для работы с пользователями.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Инициализация сервиса для работы с пользователями.

        Args:
            db (AsyncSession): Сессия базы данных
        """
        self._repository = UserRepository(db)

    async def register(self, payload: UserRegisterData) -> dict | None:
        """
        Регистрация пользователя.

        Args:
            payload (UserRegisterData): Данные для регистрации пользователя.

        Returns:
            (dict | None): Данные пользователя. None, если пользователь не создан.

        Raises:
            LoginConflictException: Если логин уже занят.
            EmailConflictException: Если email уже занят.
        """
        await self._validate_register_payload(payload)
        return await self._repository.create(payload.model_dump())

    async def login(self, payload: UserAccessData) -> UserAuthResponseData:
        """
        Аутентификация пользователя.

        Args:
            payload (UserAccessData): Данные для аутентификации пользователя.

        Returns:
            (UserAuthResponseData): Данные аутентификации пользователя.

        Raises:
            LoginNotFoundException: Если пользователь не найден.
            PasswordIncorrectException: Если пароль неверный.
        """
        user: dict | None = await self._repository.get_by_login(payload.login)

        if not user:
            raise LoginNotFoundException(payload.login)

        if not verify_password(payload.password, str(user.get("password"))):
            raise PasswordIncorrectException()

        return UserAuthResponseData(
            access_token=create_access_token({"uuid": str(user.get("uuid"))}), refresh_token="123"
        )

    async def _validate_register_payload(self, payload: UserRegisterData) -> None:
        """
        Валидация данных для регистрации пользователя.

        Args:
            payload (UserRegisterData): Данные для регистрации пользователя.

        Raises:
            LoginConflictException: Если логин уже занят.
            EmailConflictException: Если email уже занят.
        """
        login: str = payload.login

        if await self._repository.get_by_login(login):
            raise LoginConflictException(login)

        if await self._repository.get_by_email(payload.email):
            raise EmailConflictException(payload.email)
