from sqlalchemy import Column, String, UUID, Date
from uuid import uuid4
from . import Base


class Author(Base):
    __tablename__ = 'authors'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, index=True, default=uuid4)
    name = Column(String, nullable=False)
    biography = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
