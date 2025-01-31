from pydantic import BaseModel, UUID4
from datetime import date
from typing import Optional


class LoanBase(BaseModel):
    book_id: UUID4
    user_id: UUID4
    loan_date: date

    class Config:
        arbitrary_types_allowed = True


class LoanCreate(LoanBase):
    pass


class Loan(LoanBase):
    id: UUID4
    return_date: Optional[date] = None

    class Config:
        from_attributes = True
