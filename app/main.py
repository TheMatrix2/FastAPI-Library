from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, authors, books, loans, readers
from app.core.config import settings
from app.core.logging import setup_logging

# Configure application logging
setup_logging()

app = FastAPI(
    title="Library Catalog Management System",
    description="API for managing a library catalog including books, authors, readers, and loans",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API routers
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(authors.router, prefix="/api", tags=["authors"])
app.include_router(books.router, prefix="/api", tags=["books"])
app.include_router(readers.router, prefix="/api", tags=["readers"])
app.include_router(loans.router, prefix="/api", tags=["loans"])


@app.get("/", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Library Management System API is running"}