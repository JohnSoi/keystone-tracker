from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: int


class TimeStampSchemaMixin(BaseModel):
    created_at: datetime
    updated_at: datetime


class SoftDeleteSchemaMixin(BaseModel):
    deleted_at: datetime | None


class UUIDSchemaMixin(BaseModel):
    uuid: UUID
