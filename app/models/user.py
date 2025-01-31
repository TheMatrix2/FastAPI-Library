from sqlalchemy import Column, UUID, String, Enum
from uuid import uuid4
import enum

from . import Base


class Role(str, enum.Enum):
    admin = "admin"
    reader = "reader"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, index=True, default=uuid4)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.reader)
