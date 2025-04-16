from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_reader_service, get_current_user
from app.models.user import User
from app.schemas.reader import Reader, ReaderCreate, ReaderUpdate
from app.services.reader_service import ReaderService

router = APIRouter()


@router.post("/readers", response_model=Reader, status_code=status.HTTP_201_CREATED)
async def create_reader(
        reader: ReaderCreate,
        reader_service: ReaderService = Depends(get_reader_service),
        current_user: User = Depends(get_current_user),
):
    """
    Create a new reader.
    """
    return await reader_service.create_reader(reader)


@router.get("/readers", response_model=List[Reader])
async def get_readers(
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
        email: Optional[str] = None,
        reader_service: ReaderService = Depends(get_reader_service),
        current_user: User = Depends(get_current_user),
):
    """
    Retrieve all readers with optional filtering.
    """
    return await reader_service.get_readers(
        skip=skip, limit=limit
    )


@router.get("/readers/{reader_id}", response_model=Reader)
async def get_reader(
        reader_id: int,
        reader_service: ReaderService = Depends(get_reader_service),
        current_user: User = Depends(get_current_user),
):
    """
    Get a specific reader by ID.
    """
    reader = await reader_service.get_reader(reader_id)
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reader not found",
        )
    return reader


@router.put("/readers/{reader_id}", response_model=Reader)
async def update_reader(
        reader_id: int,
        reader_data: ReaderUpdate,
        reader_service: ReaderService = Depends(get_reader_service),
        current_user: User = Depends(get_current_user),
):
    """
    Update a reader.
    """
    reader = await reader_service.get_reader(reader_id)
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reader not found",
        )

    updated_reader = await reader_service.update_reader(reader_id, reader_data)
    return updated_reader


@router.delete("/readers/{reader_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reader(
        reader_id: int,
        reader_service: ReaderService = Depends(get_reader_service),
        current_user: User = Depends(get_current_user),
):
    """
    Delete a reader.
    """
    reader = await reader_service.get_reader(reader_id)
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reader not found",
        )

    await reader_service.delete_reader(reader_id)