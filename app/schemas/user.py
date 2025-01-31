from pydantic import BaseModel, Field
from typing import Optional

from app.models.user import Role


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

    class Config:
        arbitrary_types_allowed = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=6, max_length=100)


class User(UserBase):
    id: int
    role: Role = Role.reader

    class Config:
        from_attributes = True
