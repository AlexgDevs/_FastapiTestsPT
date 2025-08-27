from os import getenv

from dotenv import load_dotenv
from pytest_asyncio import fixture
from aiohttp import ClientSession

from ..db import Base

load_dotenv()

@fixture
async def get_client_session():
    session = ClientSession()
    yield session
    session.close()
