"""Пакет базового функционала приложения."""
from .schema import BaseSchema, UUIDSchemaMixin, TimeStampSchemaMixin, SoftDeleteSchemaMixin
from .exceptions import BaseHttpException, NotValidEntityException