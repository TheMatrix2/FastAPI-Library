from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.author import Author


class AuthorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, author: Author) -> Author:
        self.session.add(author)
        await self.session.commit()
        await self.session.refresh(author)
        return author

    async def get_by_id(self, author_id: int) -> Optional[Author]:
        result = await self.session.execute(
            select(Author).where(Author.id == author_id)
        )
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Author]:
        result = await self.session.execute(
            select(Author).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update(self, author: Author) -> Author:
        await self.session.commit()
        await self.session.refresh(author)
        return author

    async def delete(self, author_id: int) -> bool:
        author = await self.get_by_id(author_id)
        if author:
            await self.session.delete(author)
            await self.session.commit()
            return True
        return False
