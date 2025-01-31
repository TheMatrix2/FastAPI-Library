from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import User as UserSchema, UserCreate

from app.core.database import get_db
from app.crud.user import create_user, get_user_by_username
from app.utils.hash import verify_password
from app.utils.security import create_access_token

router = APIRouter(prefix="/auth", tags=["users"])

@router.post("/register", response_model=UserSchema)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db, user)


@router.post("/login", response_model=UserSchema)
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user_data.username)
    if not db_user or not verify_password(user_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.id, "role": db_user.role})

    return {"access_token": access_token, "token_type": "bearer"}
