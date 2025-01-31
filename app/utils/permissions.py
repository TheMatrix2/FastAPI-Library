from fastapi import Depends, HTTPException, status
from app.utils.security import get_current_user
from app.models import User

def is_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admins only"
        )
    return current_user