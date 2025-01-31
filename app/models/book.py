from sqlalchemy import Column, UUID, String, ForeignKey, Date, Integer, Table
from sqlalchemy.orm import relationship
from uuid import uuid4
from . import Base

book_author = Table(
    "book_author",
    Base.metadata,
    Column('book_id', UUID, ForeignKey("books.id"), primary_key=True),
    Column('author_id', UUID, ForeignKey("authors.id"), primary_key=True)
)


class Book(Base):
    __tablename__ = 'books'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, index=True, default=uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    publication_date = Column(Date, nullable=False)
    available_copies = Column(Integer, nullable=False, default=0)
    authors = relationship('Author', secondary=book_author, back_populates='books')
