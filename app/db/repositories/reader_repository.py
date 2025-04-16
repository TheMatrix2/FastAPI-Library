from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.reader import Reader


class ReaderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, reader: Reader) -> Reader:
        self.session.add(reader)
        await self.session.commit()
        await self.session.refresh(reader)
        return reader

    async def get_by_id(self, reader_id: int) -> Optional[Reader]:
        result = await self.session.execute(
            select(Reader).where(Reader.id == reader_id).options(joinedload(Reader.user))
        )
        return result.scalars().first()

    async def get_by_user_id(self, user_id: int) -> Optional[Reader]:
        result = await self.session.execute(
            select(Reader).where(Reader.user_id == user_id)
        )
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Reader]:
        result = await self.session.execute(
            select(Reader).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update(self, reader: Reader) -> Reader:
        await self.session.commit()
        await self.session.refresh(reader)
        return reader

    async def delete(self, reader_id: int) -> bool:
        reader = await self.get_by_id(reader_id)
        if reader:
            await self.session.delete(reader)
            await self.session.commit()
            return True
        return False
