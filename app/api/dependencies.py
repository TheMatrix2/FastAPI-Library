from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.repositories.author_repository import AuthorRepository
from app.db.repositories.book_repository import BookRepository
from app.db.repositories.loan_repository import LoanRepository
from app.db.repositories.reader_repository import ReaderRepository
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import TokenData
from app.services.auth_service import AuthService
from app.services.author_service import AuthorService
from app.services.book_service import BookService
from app.services.loan_service import LoanService
from app.services.reader_service import ReaderService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# Auth dependencies
async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    """Dependency for getting the auth service."""
    return AuthService(db)


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        auth_service: AuthService = Depends(get_auth_service),
) -> User:
    """Dependency for getting the current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await auth_service.get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception

    return user


# Author dependencies
async def get_author_repository(db: AsyncSession = Depends(get_db)) -> AuthorRepository:
    """Dependency for getting the author repository."""
    return AuthorRepository(db)


async def get_author_service(
        repo: AuthorRepository = Depends(get_author_repository),
) -> AuthorService:
    """Dependency for getting the author service."""
    return AuthorService(repo)


# Book dependencies
async def get_book_repository(db: AsyncSession = Depends(get_db)) -> BookRepository:
    """Dependency for getting the book repository."""
    return BookRepository(db)


async def get_book_service(
        repo: BookRepository = Depends(get_book_repository),
) -> BookService:
    """Dependency for getting the book service."""
    return BookService(repo)


# Reader dependencies
async def get_reader_repository(db: AsyncSession = Depends(get_db)) -> ReaderRepository:
    """Dependency for getting the reader repository."""
    return ReaderRepository(db)


async def get_reader_service(
        repo: ReaderRepository = Depends(get_reader_repository),
) -> ReaderService:
    """Dependency for getting the reader service."""
    return ReaderService(repo)


# Loan dependencies
async def get_loan_repository(
        db: AsyncSession = Depends(get_db),
        book_repo: BookRepository = Depends(get_book_repository),
) -> LoanRepository:
    """Dependency for getting the loan repository."""
    return LoanRepository(db, book_repo)


async def get_loan_service(
        repo: LoanRepository = Depends(get_loan_repository),
) -> LoanService:
    """Dependency for getting the loan service."""
    return LoanService(repo)