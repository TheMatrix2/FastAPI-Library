from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.book_repository import BookRepository
from app.db.repositories.author_repository import AuthorRepository
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate, BookWithDetails


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = BookRepository(session)
        self.author_repository = AuthorRepository(session)

    async def create_book(self, book_data: BookCreate) -> Book:
        # Verify author exists
        author = await self.author_repository.get_by_id(book_data.author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with ID {book_data.author_id} not found"
            )

        book = Book(
            title=book_data.title,
            isbn=book_data.isbn,
            description=book_data.description,
            publication_year=book_data.publication_year,
            quantity=book_data.quantity,
            author_id=book_data.author_id
        )
        return await self.repository.create(book)

    async def get_book(self, book_id: int) -> Book:
        book = await self.repository.get_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found"
            )
        return book

    async def get_book_with_details(self, book_id: int) -> BookWithDetails:
        book = await self.get_book(book_id)
        available_quantity = await self.repository.get_available_quantity(book_id)

        # Create response with author name and available quantity
        return BookWithDetails(
            id=book.id,
            title=book.title,
            isbn=book.isbn,
            description=book.description,
            publication_year=book.publication_year,
            quantity=book.quantity,
            author_id=book.author_id,
            author_name=f"{book.author.first_name} {book.author.last_name}",
            available_quantity=available_quantity
        )

    async def get_books(
            self,
            skip: int = 0,
            limit: int = 100,
            title: Optional[str] = None,
            author_id: Optional[int] = None,
            isbn: Optional[str] = None
    ) -> List[Book]:
        return await self.repository.get_all(
            skip=skip,
            limit=limit,
            title=title,
            author_id=author_id,
            isbn=isbn
        )

    async def update_book(self, book_id: int, book_data: BookUpdate) -> Book:
        book = await self.get_book(book_id)

        # Update fields if provided
        if book_data.title is not None:
            book.title = book_data.title
        if book_data.isbn is not None:
            book.isbn = book_data.isbn
        if book_data.description is not None:
            book.description = book_data.description
        if book_data.publication_year is not None:
            book.publication_year = book_data.publication_year
        if book_data.quantity is not None:
            book.quantity = book_data.quantity
        if book_data.author_id is not None:
            # Verify author exists
            author = await self.author_repository.get_by_id(book_data.author_id)
            if not author:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Author with ID {book_data.author_id} not found"
                )
            book.author_id = book_data.author_id

        return await self.repository.update(book)

    async def delete_book(self, book_id: int) -> bool:
        success = await self.repository.delete(book_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found"
            )
        return True

    async def check_book_availability(self, book_id: int) -> int:
        """Check how many copies of a book are available for loan."""
        # First verify book exists
        book = await self.repository.get_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found"
            )

        return await self.repository.get_available_quantity(book_id)
