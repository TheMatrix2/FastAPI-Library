from fastapi import HTTPException

class NotFoundException(HTTPException):
    def __init__(self, detail="Resource not found"):
        super().__init__(status_code=404, detail=detail)

class AlreadyExistsException(HTTPException):
    def __init__(self, detail="Resource already exists"):
        super().__init__(status_code=400, detail=detail)