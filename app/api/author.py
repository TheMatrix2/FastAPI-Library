from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import UUID4

from app.core.database import get_db
from app.schemas.author import Author as AuthorSchema, AuthorCreate
from app.crud.author import create_author, get_author, get_authors, update_author, delete_author
from app.utils.permissions import is_admin

router = APIRouter(prefix="/authors", tags=["authors"])

@router.post("/", response_model=AuthorSchema)
def create(author: AuthorCreate,
                  db: Session = Depends(get_db),
                  current_user=Depends(is_admin)):
    return create_author(db, author)

@router.get("/", response_model=list[AuthorSchema])
def get(skip: int = 0, limit: int = 10,
                db: Session = Depends(get_db),
                current_user=Depends(is_admin)):
    return get_authors(db, skip, limit)

@router.get("/{author_id}", response_model=AuthorSchema)
def get_all(author_id: UUID4,
               db: Session = Depends(get_db),
               current_user=Depends(is_admin)):
    return get_author(db, author_id)

@router.put("/{author_id}", response_model=AuthorSchema)
def update(author_id: UUID4,
                  author: AuthorCreate,
                  db: Session = Depends(get_db),
                  current_user=Depends(is_admin)):
    return update_author(db, author_id, author)

@router.delete("/{author_id}")
def delete(author_id: UUID4,
                  db: Session = Depends(get_db),
                  current_user=Depends(is_admin)):
    return delete_author(db, author_id)