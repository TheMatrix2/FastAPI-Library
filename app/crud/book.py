from sqlalchemy.orm import Session

from app.models.book import Book
from app.schemas.book import BookCreate
from app.utils.exceptions import *


def create_book(db: Session, book: BookCreate):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise NotFoundException("Book not found")
    return book

def get_books(db: Session, skip: int = 0, limit: int = 10, genre: str = None):
    query = db.query(Book)
    if genre:
        query = query.filter(Book.genre == genre)
    return query.offset(skip).limit(limit).all()

def update_book(db: Session, book_id: int, book_data: BookCreate):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise NotFoundException("Book not found")

    for key, value in book_data.model_dump().items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise NotFoundException("Book not found")

    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}
