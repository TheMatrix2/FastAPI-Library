from typing import Optional
from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str
    isbn: str
    description: Optional[str] = None
    publication_year: Optional[int] = None
    quantity: int = 1
    author_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    title: Optional[str] = None
    isbn: Optional[str] = None
    description: Optional[str] = None
    publication_year: Optional[int] = None
    quantity: Optional[int] = None
    author_id: Optional[int] = None


class BookInDBBase(BookBase):
    id: int

    class Config:
        from_attributes = True


class Book(BookInDBBase):
    pass


class BookWithDetails(Book):
    author_name: str = Field(None, description="Author's full name")
    available_quantity: int = Field(0, description="Books available for loan")
