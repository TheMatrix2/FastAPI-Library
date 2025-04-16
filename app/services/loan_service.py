import datetime
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.loan_repository import LoanRepository
from app.db.repositories.book_repository import BookRepository
from app.db.repositories.reader_repository import ReaderRepository
from app.models.loan import Loan, LoanStatus
from app.schemas.loan import LoanCreate, LoanUpdate, LoanWithDetails


class LoanService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = LoanRepository(session)
        self.book_repository = BookRepository(session)
        self.reader_repository = ReaderRepository(session)

    async def create_loan(self, loan_data: LoanCreate) -> Loan:
        # Verify book exists and is available
        book = await self.book_repository.get_by_id(loan_data.book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {loan_data.book_id} not found"
            )

        available_quantity = await self.book_repository.get_available_quantity(loan_data.book_id)
        if available_quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Book with ID {loan_data.book_id} is not available for loan"
            )

        # Verify reader exists
        reader = await self.reader_repository.get_by_id(loan_data.reader_id)
        if not reader:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reader with ID {loan_data.reader_id} not found"
            )

        # Create loan with default due date of 14 days if not specified
        due_date = loan_data.due_date or (datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=14))

        loan = Loan(
            book_id=loan_data.book_id,
            reader_id=loan_data.reader_id,
            loan_date=loan_data.loan_date or datetime.datetime.now(datetime.UTC),
            due_date=due_date,
            status=LoanStatus.BORROWED
        )
        return await self.repository.create(loan)

    async def get_loan(self, loan_id: int) -> Loan:
        loan = await self.repository.get_by_id(loan_id)
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Loan with ID {loan_id} not found"
            )
        return loan

    async def get_loan_with_details(self, loan_id: int) -> LoanWithDetails:
        loan = await self.get_loan(loan_id)

        # Create response with book title and reader name
        return LoanWithDetails(
            id=loan.id,
            book_id=loan.book_id,
            reader_id=loan.reader_id,
            loan_date=loan.loan_date,
            due_date=loan.due_date,
            return_date=loan.return_date,
            status=loan.status,
            book_title=loan.book.title,
            reader_name=f"{loan.reader.first_name} {loan.reader.last_name}"
        )

    async def get_loans(
            self,
            skip: int = 0,
            limit: int = 100,
            reader_id: Optional[int] = None,
            book_id: Optional[int] = None,
            status: Optional[LoanStatus] = None
    ) -> List[Loan]:
        return await self.repository.get_all(
            skip=skip,
            limit=limit,
            reader_id=reader_id,
            book_id=book_id,
            status=status
        )

    async def update_loan(self, loan_id: int, loan_data: LoanUpdate) -> Loan:
        loan = await self.get_loan(loan_id)

        # Update fields if provided
        if loan_data.book_id is not None:
            # Verify book exists
            book = await self.book_repository.get_by_id(loan_data.book_id)
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Book with ID {loan_data.book_id} not found"
                )
            loan.book_id = loan_data.book_id

        if loan_data.reader_id is not None:
            # Verify reader exists
            reader = await self.reader_repository.get_by_id(loan_data.reader_id)
            if not reader:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Reader with ID {loan_data.reader_id} not found"
                )
            loan.reader_id = loan_data.reader_id

        if loan_data.loan_date is not None:
            loan.loan_date = loan_data.loan_date
        if loan_data.due_date is not None:
            loan.due_date = loan_data.due_date
        if loan_data.return_date is not None:
            loan.return_date = loan_data.return_date
        if loan_data.status is not None:
            loan.status = loan_data.status

        return await self.repository.update(loan)

    async def delete_loan(self, loan_id: int) -> bool:
        success = await self.repository.delete(loan_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Loan with ID {loan_id} not found"
            )
        return True

    async def return_book(self, loan_id: int) -> Loan:
        loan = await self.repository.mark_as_returned(loan_id)
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Loan with ID {loan_id} not found or already returned"
            )
        return loan

    async def update_overdue_loans(self) -> int:
        """Update status of all overdue loans."""
        return await self.repository.update_overdue_loans()
