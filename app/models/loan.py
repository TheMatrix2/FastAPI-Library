import enum
from datetime import datetime
from sqlalchemy import Column, Enum, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class LoanStatus(str, enum.Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"
    OVERDUE = "overdue"


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    loan_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    status = Column(Enum(LoanStatus), nullable=False, default=LoanStatus.BORROWED)

    # Relationships
    book = relationship("Book", back_populates="loans")
    reader = relationship("Reader", back_populates="loans")

    def __repr__(self):
        return f"Loan {self.id}: {self.book.title} to {self.reader.first_name} {self.reader.last_name}"