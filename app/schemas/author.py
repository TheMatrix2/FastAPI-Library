from pydantic import BaseModel, UUID4, Field
from datetime import date
from typing import Optional

class AuthorBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    biography: Optional[str] = None
    birth_date: Optional[date] = None

    class Config:
        arbitrary_types_allowed = True


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: UUID4

    class Config:
        from_attributes = True
