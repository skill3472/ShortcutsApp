from pydantic import BaseModel
from datetime import datetime


class LoginRequest(BaseModel):
    username: str
    password: str


class AdminUserDTO(BaseModel):
    id: int
    username: str
    created_at: datetime
