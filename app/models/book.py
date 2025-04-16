from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    isbn = Column(String(13), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    publication_year = Column(Integer, nullable=True)
    quantity = Column(Integer, default=1, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    # Relationships
    author = relationship("Author", back_populates="books")
    loans = relationship("Loan", back_populates="book")

    def __repr__(self):
        return f"{self.title} ({self.isbn})"
