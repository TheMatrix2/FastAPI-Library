from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.book import Book as BookSchema, BookCreate, Book
from app.crud.book import create_book, get_books, get_book, update_book, delete_book
from app.utils.permissions import is_admin

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=BookSchema)
def create(book: BookCreate, db: Session = Depends(get_db), current_user=Depends(is_admin)):
    return create_book(db, book)

@router.get("/", response_model=list[BookSchema])
def get(skip: int = 0, limit: int = 10, genre: str = None, db: Session = Depends(get_db)):
    return get_books(db, skip, limit, genre)

@router.get("/{book_id}", response_model=BookSchema)
def get_all(book_id: int, db: Session = Depends(get_db)):
    return get_book(db, book_id)

@router.put("/{book_id}", response_model=BookSchema)
def update(book_id: int, book: BookCreate, db: Session = Depends(get_db), current_user=Depends(is_admin)):
    return update_book(db, book_id, book)

@router.delete("/{book_id}")
def delete(book_id: int, db: Session = Depends(get_db), current_user=Depends(is_admin)):
    return delete_book(db, book_id)