import pytest
from fastapi.testclient import TestClient
from typing import Dict, Callable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app
from app.core.config import settings

SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides: Dict[Callable, Callable] = {get_db: override_get_db}
    settings.database_uri = SQLALCHEMY_DATABASE_URI
    return TestClient(app)


