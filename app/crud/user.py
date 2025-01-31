from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import User, Role
from app.schemas.user import UserCreate, UserUpdate
from app.utils.hash import hash_password
from app.utils.exceptions import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, password_hash=hashed_password, role=Role.reader)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, new_user: UserUpdate):
    db_user = db.query(User).filter(User.id == new_user.id).first()
    if db_user:
        db_user.username = new_user.username
        db_user.hashed_password = hash_password(new_user.password)
        db.commit()
        db.refresh(db_user)
    return db_user


def get_readers(db: Session):
    return db.query(User).filter(User.role == Role.reader).all()


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException("User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
