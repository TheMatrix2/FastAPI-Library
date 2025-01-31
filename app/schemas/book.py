from pydantic import BaseModel, UUID4, Field
from datetime import date
from typing import List, Optional

from app.models.author import Author



class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    publication_date: date
    genre: List[str]
    available_copies: int = Field(..., ge=0)

    class Config:
        arbitrary_types_allowed = True


class BookCreate(BookBase):
    author_ids: List[UUID4]


class Book(BookBase):
    id: UUID4
    authors: List[Author]

    class Config:
        from_attributes = True
