from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    login: str
    password: str
    email: str


class StatusSuccess(BaseModel):
    pass


class UserInfo(BaseModel):
    email: str
    login: str
    last_loging: Optional[datetime]
    role_name: Optional[str]

    class Config:
        from_attributes = True


class UsersInfo(BaseModel):
    users: List[UserInfo]

