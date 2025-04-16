from typing import List, Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.book import Book
from app.models.loan import Loan, LoanStatus


class BookRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, book: Book) -> Book:
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def get_by_id(self, book_id: int) -> Optional[Book]:
        result = await self.session.execute(
            select(Book).where(Book.id == book_id).options(joinedload(Book.author))
        )
        return result.scalars().first()

    async def get_all(
            self,
            skip: int = 0,
            limit: int = 100,
            title: Optional[str] = None,
            author_id: Optional[int] = None,
            isbn: Optional[str] = None
    ) -> List[Book]:
        query = select(Book).options(joinedload(Book.author))

        if title:
            query = query.where(Book.title.ilike(f"%{title}%"))
        if author_id:
            query = query.where(Book.author_id == author_id)
        if isbn:
            query = query.where(Book.isbn == isbn)

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, book: Book) -> Book:
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def delete(self, book_id: int) -> bool:
        book = await self.get_by_id(book_id)
        if book:
            await self.session.delete(book)
            await self.session.commit()
            return True
        return False

    async def get_available_quantity(self, book_id: int) -> int:
        book = await self.get_by_id(book_id)
        if not book:
            return 0

        # Count active loans
        result = await self.session.execute(
            select(func.count()).where(
                Loan.book_id == book_id,
                Loan.status.in_([LoanStatus.BORROWED, LoanStatus.OVERDUE])
            )
        )
        active_loans = result.scalar()

        return max(0, book.quantity - active_loans)
