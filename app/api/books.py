from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_book_service, get_current_user
from app.models.user import User
from app.schemas.book import Book, BookCreate, BookUpdate
from app.services.book_service import BookService

router = APIRouter()


@router.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(
        book: BookCreate,
        book_service: BookService = Depends(get_book_service),
        current_user: User = Depends(get_current_user),
):
    """
    Create a new book.
    """
    return await book_service.create_book(book)


@router.get("/books", response_model=List[Book])
async def get_books(
        skip: int = 0,
        limit: int = 100,
        title: Optional[str] = None,
        author_id: Optional[int] = None,
        isbn: Optional[str] = None,
        genre: Optional[str] = None,
        available: Optional[bool] = None,
        book_service: BookService = Depends(get_book_service),
):
    """
    Retrieve books with optional filtering.
    """
    return await book_service.get_books(
        skip=skip,
        limit=limit,
        title=title,
        author_id=author_id,
        isbn=isbn,
    )


@router.get("/books/{book_id}", response_model=Book)
async def get_book(
        book_id: int,
        book_service: BookService = Depends(get_book_service),
):
    """
    Get a specific book by ID.
    """
    book = await book_service.get_book_with_details(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return book


@router.put("/books/{book_id}", response_model=Book)
async def update_book(
        book_id: int,
        book_data: BookUpdate,
        book_service: BookService = Depends(get_book_service),
        current_user: User = Depends(get_current_user),
):
    """
    Update a book.
    """
    book = await book_service.get_book(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    updated_book = await book_service.update_book(book_id, book_data)
    return updated_book


@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
        book_id: int,
        book_service: BookService = Depends(get_book_service),
        current_user: User = Depends(get_current_user),
):
    """
    Delete a book.
    """
    book = await book_service.get_book(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    await book_service.delete_book(book_id)