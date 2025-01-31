from sqlalchemy.orm import Session
from pydantic import UUID4

from app.models.author import Author as AuthorModel
from app.schemas.author import Author as AuthorSchema, AuthorCreate
from app.utils.exceptions import NotFoundException


def create_author(db: Session, author: AuthorCreate):
    db_author = AuthorSchema(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session, author_id: UUID4):
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not author:
        raise NotFoundException("Author not found")
    return author


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(AuthorModel).offset(skip).limit(limit).all()


def update_author(db: Session, author_id: UUID4, author_data: AuthorCreate):
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not author:
        raise NotFoundException("Author not found")

    for key, value in author_data.model_dump().items():
        setattr(author, key, value)

    db.commit()
    db.refresh(author)
    return author


def delete_author(db: Session, author_id: UUID4):
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not author:
        raise NotFoundException("Author not found")

    db.delete(author)
    db.commit()
    return {"message": "Author deleted successfully"}