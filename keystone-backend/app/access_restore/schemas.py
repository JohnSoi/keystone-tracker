from pydantic import BaseModel


class AccessRestoreData(BaseModel):
    user_id: int
    user_deleted: bool
    user_email: str
