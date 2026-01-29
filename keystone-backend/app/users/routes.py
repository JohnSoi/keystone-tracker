from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from .schemas import UserRegisterData, UserPublicData

user_routes: APIRouter = APIRouter(prefix="/user", tags=["user"])


@user_routes.post("/register", description="Регистрация нового пользователя", response_model=UserPublicData)
def user_register(user_data: UserRegisterData, db: AsyncSession = Depends(get_db)):
    return user_data
