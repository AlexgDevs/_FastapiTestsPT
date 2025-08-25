import asyncio
from fastapi import FastAPI

from .db import db_manager, get_db


async def main_db():
    await db_manager.migrate()
    await db_manager.up()

app = FastAPI()

