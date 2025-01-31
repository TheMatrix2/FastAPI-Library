from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import UUID4

from app.core.database import get_db
from app.schemas.loan import Loan as LoanSchema, LoanCreate
from app.utils.security import get_current_user
from app.models import User
from app.crud.loan import create_loan, get_loans, return_book

router = APIRouter(prefix="/loans", tags=["loans"])


@router.post("/", response_model=LoanSchema)
def create(
    loan_data: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_loan(db, loan_data)


@router.get("/", response_model=list[LoanSchema])
def get(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_loans(db, skip, limit)


@router.put("/{loan_id}/return")
def update(
    loan_id: UUID4,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return return_book(db, loan_id)