from typing import List, Optional
from pydantic import BaseModel


class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    biography: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    biography: Optional[str] = None


class AuthorResponse(AuthorBase):
    id: int


class AuthorInDBBase(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class Author(AuthorInDBBase):
    pass


class AuthorWithBooks(Author):
    from app.schemas.book import Book
    books: List[Book] = []
