from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

Base = declarative_base()

# Define all models here for Alembic
from app.models.user import User
from app.models.author import Author
from app.models.book import Book
from app.models.reader import Reader
from app.models.loan import Loan