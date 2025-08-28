from os import getenv

from dotenv import load_dotenv
from pytest_asyncio import fixture
from aiohttp import ClientSession

from ..db import Base

load_dotenv()

@fixture
async def get_client_session():
    async with ClientSession('http://127.0.0.1:8000') as session:
        yield session