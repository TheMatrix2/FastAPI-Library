from fastapi import FastAPI

from app.api import auth, user, book, author, loan
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Library API')

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(book.router)
app.include_router(loan.router)
app.include_router(author.router)