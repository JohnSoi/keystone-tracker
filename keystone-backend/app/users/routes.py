"""Модуль роутов для работы с пользователями."""

from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from .dependencies import get_current_user
from .model import User as UserModel
from .schemas import UserAccessData, UserAuthResponseData, UserPasswordData, UserPublicData, UserRegisterData
from .service import UserService

user_routes: APIRouter = APIRouter(prefix="/user", tags=["user"])


@user_routes.post("/register", description="Регистрация нового пользователя", response_model=UserPublicData)
async def user_register(user_data: UserRegisterData, db: AsyncSession = Depends(get_db)) -> dict | None:
    """Регистрация нового пользователя."""
    return await UserService[UserRegisterData](db).register(user_data)


@user_routes.post("/login", description="Аутентификация пользователя", response_model=UserAuthResponseData)
async def user_login(
    response: Response, user_data: UserAccessData, db: AsyncSession = Depends(get_db)
) -> UserAuthResponseData:
    """Аутентификация пользователя."""
    return await UserService(db).login(user_data, response)


@user_routes.post("/confirm/send", description="Выход пользователя")
async def user_confirm_send(user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> bool:
    """Повторная отправка письма для подтверждения почты."""
    return await UserService(db).send_confirm_email(user)


@user_routes.post("/confirm/{confirm_token}", description="Подтверждение почты пользователя")
async def user_email_confirm(confirm_token: UUID, db: AsyncSession = Depends(get_db)) -> bool:
    """Подтверждение почты пользователя."""
    return await UserService(db).confirm_email(confirm_token)


@user_routes.post("/restore-access", description="Восстановление доступа пользователя")
async def user_restore_access(user_email: str, db: AsyncSession = Depends(get_db)) -> bool:
    """Восстановление доступа пользователя."""
    return await UserService(db).restore_access(user_email)


@user_routes.post("/restore-access/{restore_token}", description="Восстановление доступа пользователя по токену")
async def user_restore_access_by_token(
    restore_token: UUID, payload: UserPasswordData, db: AsyncSession = Depends(get_db)
) -> bool:
    """Восстановление доступа пользователя по токену."""
    return await UserService(db).restore_access_by_token(restore_token, payload.password)


@user_routes.delete("/delete", description="Удаление пользователя")
async def user_delete(
    request: Request, user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_db)
) -> bool:
    """Удаление аутентифицированного пользователя из системы."""
    return await UserService(db, request).delete(user.id)


@user_routes.patch("/update", description="Обновление данных пользователя")
async def user_update(
    request: Request,
    user_data: UserPublicData,
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(get_current_user),
) -> UserPublicData:
    """Обновление данных пользователя."""
    return await UserService[UserPublicData](db, request).update(user.id, user_data)


@user_routes.get("/me", description="Получение данных текущего пользователя", response_model=UserPublicData)
async def user_me(request: Request, _: UserModel = Depends(get_current_user)) -> UserPublicData:
    """Получение данных текущего пользователя."""
    return UserPublicData(**request.state.user.to_dict())
