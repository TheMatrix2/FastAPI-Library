from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    biography = Column(Text, nullable=True)

    # Relationships
    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
