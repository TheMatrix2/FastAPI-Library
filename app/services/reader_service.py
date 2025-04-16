from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.reader_repository import ReaderRepository
from app.db.repositories.loan_repository import LoanRepository
from app.services.auth_service import AuthService
from app.models.reader import Reader
from app.schemas.reader import ReaderCreate, ReaderUpdate


class ReaderService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ReaderRepository(session)
        self.loan_repository = LoanRepository(session)
        self.auth_service = AuthService(session)

    async def create_reader(self, reader_data: ReaderCreate) -> Reader:
        # Verify user exists
        user = await self.auth_service.get_user_by_id(reader_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {reader_data.user_id} not found"
            )

        # Check if user already has a reader profile
        existing_reader = await self.repository.get_by_user_id(reader_data.user_id)
        if existing_reader:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with ID {reader_data.user_id} already has a reader profile"
            )

        reader = Reader(
            first_name=reader_data.first_name,
            last_name=reader_data.last_name,
            phone_number=reader_data.phone_number,
            user_id=reader_data.user_id
        )
        return await self.repository.create(reader)

    async def get_reader(self, reader_id: int) -> Reader:
        reader = await self.repository.get_by_id(reader_id)
        if not reader:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reader with ID {reader_id} not found"
            )
        return reader

    async def get_reader_by_user_id(self, user_id: int) -> Reader:
        reader = await self.repository.get_by_user_id(user_id)
        if not reader:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reader profile for user with ID {user_id} not found"
            )
        return reader

    async def get_readers(self, skip: int = 0, limit: int = 100) -> List[Reader]:
        return await self.repository.get_all(skip=skip, limit=limit)

    async def update_reader(self, reader_id: int, reader_data: ReaderUpdate) -> Reader:
        reader = await self.get_reader(reader_id)

        # Update fields if provided
        if reader_data.first_name is not None:
            reader.first_name = reader_data.first_name
        if reader_data.last_name is not None:
            reader.last_name = reader_data.last_name
        if reader_data.phone_number is not None:
            reader.phone_number = reader_data.phone_number

        return await self.repository.update(reader)

    async def delete_reader(self, reader_id: int) -> bool:
        success = await self.repository.delete(reader_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reader with ID {reader_id} not found"
            )
        return True
