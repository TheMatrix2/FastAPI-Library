from fastapi import APIRouter, Depends

from app.schemas.user import User as UserSchema, UserUpdate

from app.models.user import User as UserModel
from app.core.database import get_db
from app.crud.user import *
from app.utils.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/readers", response_model=list[UserSchema])
def show_readers(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You are not authorized to view this")
    return get_readers(db)


@router.get("/me", response_model=UserSchema)
def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


@router.put("/update", response_model=UserSchema)
def update(user: UserUpdate, db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):
    db_user = get_user_by_username(db, user.username)
    if db_user is None or db_user.id != current_user.id:
        raise HTTPException(status_code=404, detail="User not found")
    return update_user(db_user)


@router.delete("/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)
