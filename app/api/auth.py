from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.auth import Token, User as UserSchema, UserCreate
from app.services.auth_service import AuthService, get_current_user, get_current_active_admin

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserSchema)
async def register_user(
        user_data: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    user = await auth_service.create_user(user_data)
    return user


@router.post("/register/admin", response_model=UserSchema)
async def register_admin(
        user_data: UserCreate,
        current_user: User = Depends(get_current_active_admin),
        db: AsyncSession = Depends(get_db)
):
    user_data.role = UserRole.ADMIN
    auth_service = AuthService(db)
    user = await auth_service.create_user(user_data)
    return user


@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
