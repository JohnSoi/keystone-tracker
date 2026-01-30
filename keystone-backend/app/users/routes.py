from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from .schemas import UserRegisterData, UserPublicData, UserAuthResponseData, UserAccessData
from .service import UserService

user_routes: APIRouter = APIRouter(prefix="/user", tags=["user"])


@user_routes.post("/register", description="Регистрация нового пользователя", response_model=UserPublicData)
async def user_register(user_data: UserRegisterData, db: AsyncSession = Depends(get_db)):
    return await UserService(db).register(user_data)


@user_routes.post("/login", description="Аутентификация пользователя", response_model=UserAuthResponseData)
async def user_login(user_data: UserAccessData, db: AsyncSession = Depends(get_db)):
    return await UserService(db).login(user_data)
