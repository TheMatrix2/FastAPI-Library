from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.models.loan import LoanStatus


class LoanBase(BaseModel):
    book_id: int
    reader_id: int
    loan_date: datetime = datetime.utcnow()
    due_date: datetime
    status: LoanStatus = LoanStatus.BORROWED


class LoanCreate(LoanBase):
    pass


class LoanUpdate(LoanBase):
    book_id: Optional[int] = None
    reader_id: Optional[int] = None
    loan_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    status: Optional[LoanStatus] = None


class LoanInDBBase(LoanBase):
    id: int
    return_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class Loan(LoanInDBBase):
    pass


class LoanWithDetails(Loan):
    book_title: str
    reader_name: str
