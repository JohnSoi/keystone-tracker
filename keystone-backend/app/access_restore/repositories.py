from app.core.database import BaseRepository

from .model import AccessRestore as AccessRestoreModel


class AccessRestoreRepository(BaseRepository[AccessRestoreModel]):
    _MODEL = AccessRestoreModel
