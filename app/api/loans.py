from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_loan_service, get_current_user
from app.models.user import User
from app.schemas.loan import Loan, LoanCreate, LoanUpdate
from app.services.loan_service import LoanService

router = APIRouter()


@router.post("/loans", response_model=Loan, status_code=status.HTTP_201_CREATED)
async def create_loan(
        loan: LoanCreate,
        loan_service: LoanService = Depends(get_loan_service),
        current_user: User = Depends(get_current_user),
):
    """
    Create a new loan.
    """
    try:
        return await loan_service.create_loan(loan)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/loans", response_model=List[Loan])
async def get_loans(
        skip: int = 0,
        limit: int = 100,
        reader_id: Optional[int] = None,
        book_id: Optional[int] = None,
        status: Optional[str] = None,
        due_before: Optional[date] = None,
        overdue: Optional[bool] = None,
        loan_service: LoanService = Depends(get_loan_service),
        current_user: User = Depends(get_current_user),
):
    """
    Retrieve loans with optional filtering.
    """
    return await loan_service.get_loans(
        skip=skip,
        limit=limit,
        reader_id=reader_id,
        book_id=book_id,
        status=status,
    )


@router.get("/loans/{loan_id}", response_model=Loan)
async def get_loan(
        loan_id: int,
        loan_service: LoanService = Depends(get_loan_service),
        current_user: User = Depends(get_current_user),
):
    """
    Get a specific loan by ID.
    """
    loan = await loan_service.get_loan(loan_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found",
        )
    return loan


@router.put("/loans/{loan_id}", response_model=Loan)
async def update_loan(
        loan_id: int,
        loan_data: LoanUpdate,
        loan_service: LoanService = Depends(get_loan_service),
        current_user: User = Depends(get_current_user),
):
    """
    Update a loan.
    """
    loan = await loan_service.get_loan(loan_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found",
        )

    try:
        updated_loan = await loan_service.update_loan(loan_id, loan_data)
        return updated_loan
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/loans/{loan_id}/return", response_model=Loan)
async def return_book(
        loan_id: int,
        loan_service: LoanService = Depends(get_loan_service),
        current_user: User = Depends(get_current_user),
):
    """
    Return a book (mark loan as returned).
    """
    loan = await loan_service.get_loan(loan_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found",
        )

    if loan.return_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book already returned",
        )

    return await loan_service.return_book(loan_id)