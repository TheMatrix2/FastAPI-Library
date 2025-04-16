from typing import List, Optional
from pydantic import BaseModel


class ReaderBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    user_id: int


class ReaderCreate(ReaderBase):
    pass


class ReaderUpdate(ReaderBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    user_id: Optional[int] = None


class ReaderInDBBase(ReaderBase):
    id: int

    class Config:
        from_attributes = True


class Reader(ReaderInDBBase):
    pass


class ReaderWithLoans(Reader):
    from app.schemas.loan import Loan
    loans: List[Loan] = []
