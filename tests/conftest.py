import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.api import auth, authors, books, loans, readers
from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db

# Test database settings - use SQLite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create async engine for testing
test_engine = create_async_engine(
    TEST_DATABASE_URL, echo=False, future=True, connect_args={"check_same_thread": False}
)

# Create test session
TestSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


# Create a new application
@pytest_asyncio.fixture
async def app() -> FastAPI:
    """Create a test FastAPI app with routes."""
    # Create test app
    app = FastAPI()

    # Include API routers
    app.include_router(auth.router, prefix="/api", tags=["auth"])
    app.include_router(authors.router, prefix="/api", tags=["authors"])
    app.include_router(books.router, prefix="/api", tags=["books"])
    app.include_router(readers.router, prefix="/api", tags=["readers"])
    app.include_router(loans.router, prefix="/api", tags=["loans"])

    return app


# Create database tables and drop them after tests
@pytest_asyncio.fixture(autouse=True)
async def initialize_db() -> AsyncGenerator[None, None]:
    """Create tables on startup and drop them on shutdown."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Database session fixture
@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    session = TestSessionLocal()
    try:
        yield session
    finally:
        await session.close()


# Override get_db dependency
@pytest_asyncio.fixture
async def override_get_db(db_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    """Override the get_db dependency for testing."""

    async def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    return _get_test_db


# Client fixture
@pytest_asyncio.fixture
async def client(app: FastAPI, override_get_db) -> AsyncGenerator[AsyncClient, None]:
    """Create an HTTP client for testing the API."""
    # Override dependencies
    app.dependency_overrides[get_db] = override_get_db

    # Create test client
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# Auth fixtures
@pytest_asyncio.fixture
async def test_user(client: AsyncClient) -> dict:
    """Create a test user for authentication."""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    }

    response = await client.post("/api/auth/register", json=user_data)
    return response.json()


@pytest_asyncio.fixture
async def token(client: AsyncClient, test_user: dict) -> str:
    """Get authentication token for test user."""
    response = await client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "password123"},
    )
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def authorized_client(client: AsyncClient, token: str) -> AsyncClient:
    """Create an authorized client with token."""
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client