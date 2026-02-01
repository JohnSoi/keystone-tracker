# mypy: disable_error_code="arg-type"
# mypy: disable_error_code="override"
# mypy: disable_error_code="no-any-return"
"""Модуль сервиса для работы с пользователями."""

from datetime import UTC, datetime
from typing import Generic, TypeVar
from uuid import UUID

from fastapi import Response
from pydantic import BaseModel

from app.access_restore import AccessRestoreData, AccessRestoreService
from app.confirmation import ConfirmationData, ConfirmService
from app.core import BaseService, ServiceOperation, create_access_token, verify_password

from . import exceptions as exc
from .consts import ACCESS_TOKEN_COOKIE_NAME, REFRESH_TOKEN_COOKIE_NAME
from .model import User as UserModel
from .repository import UserRepository
from .schemas import UserAccessData, UserAuthResponseData, UserRegisterData
from .validators import validate_email


UserInputData = TypeVar("UserInputData", bound=BaseModel)


class UserService(Generic[UserInputData], BaseService[UserRepository, UserInputData, UserModel]):
    """Сервис для работы с пользователями."""

    _REPOSITORY = UserRepository

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
        user: UserModel = await self.create(payload)

        await ConfirmService(self._db).create(ConfirmationData(user_id=user.id, user_email=str(user.email)))

        return user.to_dict()

    async def login(self, payload: UserAccessData, response: Response) -> UserAuthResponseData:
        """
        Аутентификация пользователя.

        Args:
            payload (UserAccessData): Данные для аутентификации пользователя.
            response (Response): Объект ответа.

        Returns:
            (UserAuthResponseData): Данные аутентификации пользователя.

        Raises:
            LoginNotFoundException: Если пользователь не найден.
            PasswordIncorrectException: Если пароль неверный.
        """
        user: UserModel | None = await self._repository.get_by_login(payload.login)

        if not user:
            raise exc.LoginNotFoundException(payload.login)

        if user.is_deleted:
            raise exc.DeletedUserException()

        if not verify_password(payload.password, str(user.password)):
            raise exc.PasswordIncorrectException()

        access_token: str = create_access_token({"uuid": str(user.uuid)})
        refresh_token: str = "123"

        response.set_cookie(ACCESS_TOKEN_COOKIE_NAME, access_token)
        response.set_cookie(REFRESH_TOKEN_COOKIE_NAME, refresh_token)

        return UserAuthResponseData(access_token=access_token, refresh_token=refresh_token)

    async def restore_access(self, user_email: str) -> bool:
        """
        Запрос на восстановление доступа пользователя.

        Args:
            user_email (str): Email пользователя

        Returns:
            (bool): True, если доступ запрошен.

        Examples:
            >>> async def restore_access(ex_user_email: str) -> bool:
            ...     return await UserService().restore_access(ex_user_email)
        """
        valid_user_email: str = validate_email(user_email)

        user_data: UserModel | None = await self._repository.get_by_email(valid_user_email)

        if not user_data:
            raise exc.EmailNotFoundException(valid_user_email)

        await AccessRestoreService(self._db).create(
            AccessRestoreData(user_id=user_data.id, user_deleted=user_data.is_deleted, user_email=str(user_data.email))
        )

        return True

    async def restore_access_by_token(self, token: UUID, new_password: str) -> bool:
        """
        Восстановление доступа пользователя по токену.

        Args:
            token (UUID): Токен восстановления доступа.
            new_password (str): Новый пароль пользователя

        Returns:
            (bool): True, если доступ восстановлен.

        Examples:
            >>> async def restore_access_by_token(ex_token: UUID, ex_new_password: str) -> bool:
            ...     return await UserService().restore_access_by_token(ex_token, ex_new_password)
        """
        user_id: int = await AccessRestoreService(self._db).redeem(token)

        await self._repository.update(user_id, {"password": new_password, "deleted_at": None})

        return True

    async def send_confirm_email(self, user: UserModel) -> bool:
        """
        Отправка письма для подтверждения email пользователя.

        Args:
            user (UserModel): Пользователь.

        Returns:
            (bool): True, если письмо отправлено.

        Examples:
            >>> async def send_confirm_email(ex_user: UserModel) -> bool:
            ...     return await UserService().send_confirm_email(ex_user)
        """
        if user.verified_at:
            raise exc.UserAlreadyVerifiedException()

        await ConfirmService(self._db).create(ConfirmationData(user_id=user.id, user_email=str(user.email)))
        return True

    async def confirm_email(self, token: UUID) -> bool:
        """
        Подтверждение email пользователя.

        Args:
            token (UUID): Токен подтверждения.

        Returns:
            (bool): True, если email подтвержден.

        Examples:
            >>> async def confirm_email(ex_token: UUID) -> bool:
            ...     return await UserService().confirm_email(ex_token)
        """
        user_id: int = await ConfirmService(self._db).redeem(token)

        await self._repository.update(user_id, {"verified_at": datetime.now(UTC)})

        return True

    async def _validate_payload(
        self, operation: ServiceOperation, payload: UserRegisterData | None = None, entity: UserModel | None = None
    ) -> None:
        """Валидация данных для действий с пользователями."""
        match operation:
            case ServiceOperation.CREATE:
                if not payload:
                    return

                await self._validate_register_payload(payload)
            case ServiceOperation.DELETE:
                if not self._request or (entity and entity.id != self._request.state.user.id):
                    raise exc.ForbiddenUserException()

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
            raise exc.LoginConflictException(login)

        if await self._repository.get_by_email(payload.email):
            raise exc.EmailConflictException(payload.email)
