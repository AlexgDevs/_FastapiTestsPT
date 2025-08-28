import asyncio
from fastapi import FastAPI

from .db import db_manager
from .routers import (
    user_app,
    card_app,
    account_app
)

app = FastAPI()
app.include_router(user_app)
app.include_router(card_app)
app.include_router(account_app)