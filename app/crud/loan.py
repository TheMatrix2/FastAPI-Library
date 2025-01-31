from pydantic import UUID4
from sqlalchemy.orm import Session
import datetime
from app.models.loan import Loan as LoanModel
from app.models.book import Book as BookModel
from app.schemas.loan import LoanCreate
from app.utils.exceptions import NotFoundException, AlreadyExistsException


def create_loan(db: Session, loan_data: LoanCreate):
    book = db.query(BookModel).filter(BookModel.id == loan_data.book_id).first()
    user = db.query(LoanModel).filter(LoanModel.id == loan_data.user_id).first()

    if not book:
        raise NotFoundException("Book not found")
    if not user:
        raise NotFoundException("User not found")

    if book.available_copies <= 0:
        raise AlreadyExistsException("No available copies of this book")

    active_loans = db.query(LoanModel).filter(
        LoanModel.user_id == loan_data.user_id,
        LoanModel.return_date == None
    ).count()

    if active_loans >= 5:
        raise AlreadyExistsException("User has reached the maximum loan limit (5 books)")

    due_date = datetime.datetime.now() + datetime.timedelta(days=14)
    db_loan = LoanModel(
        book_id=loan_data.book_id,
        user_id=loan_data.user_id,
        due_date=due_date
    )

    book.available_copies -= 1

    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


def get_loans(db: Session, skip: int = 0, limit: int = 10):
    return db.query(LoanModel).offset(skip).limit(limit).all()


def return_book(db: Session, loan_id: UUID4):
    loan = db.query(LoanModel).filter(LoanModel.id == loan_id).first()
    if not loan:
        raise NotFoundException("Loan not found")
    if loan.returned:
        raise AlreadyExistsException("Book is already returned")

    loan.returned = True
    loan.return_date = datetime

    book = db.query(BookModel).filter(BookModel.id == loan.book_id).first()
    book.available_copies += 1

    db.commit()
    db.refresh(loan)
    return {"message": "Book returned successfully"}