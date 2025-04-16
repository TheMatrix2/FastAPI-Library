from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_author_service, get_current_user
from app.models.user import User
from app.schemas.author import AuthorCreate, Author, AuthorUpdate
from app.services.author_service import AuthorService

router = APIRouter()


@router.post("/authors", response_model=Author, status_code=status.HTTP_201_CREATED)
async def create_author(
        author: AuthorCreate,
        author_service: AuthorService = Depends(get_author_service),
        current_user: User = Depends(get_current_user),
):
    """
    Create a new author.
    """
    return await author_service.create_author(author)


@router.get("/authors", response_model=List[Author])
async def get_authors(
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
        author_service: AuthorService = Depends(get_author_service),
):
    """
    Retrieve all authors with optional filtering by name.
    """
    return await author_service.get_authors(skip=skip, limit=limit)


@router.get("/authors/{author_id}", response_model=Author)
async def get_author(
        author_id: int,
        author_service: AuthorService = Depends(get_author_service),
):
    """
    Get a specific author by ID.
    """
    author = await author_service.get_author(author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found",
        )
    return author


@router.put("/authors/{author_id}", response_model=Author)
async def update_author(
        author_id: int,
        author_data: AuthorUpdate,
        author_service: AuthorService = Depends(get_author_service),
        current_user: User = Depends(get_current_user),
):
    """
    Update an author.
    """
    author = await author_service.get_author(author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found",
        )

    updated_author = await author_service.update_author(author_id, author_data)
    return updated_author


@router.delete("/authors/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(
        author_id: int,
        author_service: AuthorService = Depends(get_author_service),
        current_user: User = Depends(get_current_user),
):
    """
    Delete an author.
    """
    author = await author_service.get_author(author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found",
        )

    await author_service.delete_author(author_id)