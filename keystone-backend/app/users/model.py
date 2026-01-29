from datetime import date

from sqlalchemy import String, Date, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import BaseModel, UUIDMixin, TimestampMixin, SoftDeleteMixin


class User(BaseModel, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    surname: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    patronymic: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)

    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)

    login: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)

    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
