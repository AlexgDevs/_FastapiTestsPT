import asyncio
from fastapi import FastAPI

from .db import db_manager
from .routers import (
    user_app
)

app = FastAPI()
app.include_router(user_app)



