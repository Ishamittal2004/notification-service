from pydantic import BaseModel

class NotificationCreate(BaseModel):
    user_id: int
    type: str
    message: str

class NotificationOut(NotificationCreate):
    id: str
    status: str
from pydantic import BaseModel
from typing import Literal

class NotificationRequest(BaseModel):
    user_id: str
    type: Literal["email", "sms", "in_app"]
    message: str
