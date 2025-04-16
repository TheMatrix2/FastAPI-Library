import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.loan import Loan, LoanStatus


class LoanRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, loan: Loan) -> Loan:
        self.session.add(loan)
        await self.session.commit()
        await self.session.refresh(loan)
        return loan

    async def get_by_id(self, loan_id: int) -> Optional[Loan]:
        result = await self.session.execute(
            select(Loan)
            .where(Loan.id == loan_id)
            .options(joinedload(Loan.book), joinedload(Loan.reader))
        )
        return result.scalars().first()

    async def get_all(
            self,
            skip: int = 0,
            limit: int = 100,
            reader_id: Optional[int] = None,
            book_id: Optional[int] = None,
            status: Optional[LoanStatus] = None
    ) -> List[Loan]:
        query = select(Loan).options(joinedload(Loan.book), joinedload(Loan.reader))

        if reader_id:
            query = query.where(Loan.reader_id == reader_id)
        if book_id:
            query = query.where(Loan.book_id == book_id)
        if status:
            query = query.where(Loan.status == status)

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, loan: Loan) -> Loan:
        await self.session.commit()
        await self.session.refresh(loan)
        return loan

    async def delete(self, loan_id: int) -> bool:
        loan = await self.get_by_id(loan_id)
        if loan:
            await self.session.delete(loan)
            await self.session.commit()
            return True
        return False

    async def mark_as_returned(self, loan_id: int) -> Optional[Loan]:
        loan = await self.get_by_id(loan_id)
        if loan and loan.status != LoanStatus.RETURNED:
            loan.status = LoanStatus.RETURNED
            loan.return_date = datetime.datetime.now(datetime.UTC)
            await self.session.commit()
            await self.session.refresh(loan)
        return loan

    async def update_overdue_loans(self) -> int:
        """Update status of overdue loans."""
        now = datetime.datetime.now(datetime.UTC)
        result = await self.session.execute(
            select(Loan).where(
                Loan.due_date < now,
                Loan.status == LoanStatus.BORROWED
            )
        )
        overdue_loans = result.scalars().all()

        count = 0
        for loan in overdue_loans:
            loan.status = LoanStatus.OVERDUE
            count += 1

        if count > 0:
            await self.session.commit()

        return count
