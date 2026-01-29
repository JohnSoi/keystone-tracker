from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Integer, DateTime, func, UUID as PG_UUID
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, declarative_base


class CustomModel:
    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)


class SoftDeleteMixin:
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)


class UUIDMixin:
    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, default=lambda: uuid4())


BaseModel = declarative_base(cls=CustomModel)
