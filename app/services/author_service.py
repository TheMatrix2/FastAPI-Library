from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.author_repository import AuthorRepository
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate


class AuthorService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = AuthorRepository(session)

    async def create_author(self, author_data: AuthorCreate) -> Author:
        author = Author(
            first_name=author_data.first_name,
            last_name=author_data.last_name,
            biography=author_data.biography
        )
        return await self.repository.create(author)

    async def get_author(self, author_id: int) -> Author:
        author = await self.repository.get_by_id(author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with ID {author_id} not found"
            )
        return author

    async def get_authors(self, skip: int = 0, limit: int = 100) -> List[Author]:
        return await self.repository.get_all(skip=skip, limit=limit)

    async def update_author(self, author_id: int, author_data: AuthorUpdate) -> Author:
        author = await self.get_author(author_id)

        # Update fields if provided
        if author_data.first_name is not None:
            author.first_name = author_data.first_name
        if author_data.last_name is not None:
            author.last_name = author_data.last_name
        if author_data.biography is not None:
            author.biography = author_data.biography

        return await self.repository.update(author)

    async def delete_author(self, author_id: int) -> bool:
        success = await self.repository.delete(author_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with ID {author_id} not found"
            )
        return True
