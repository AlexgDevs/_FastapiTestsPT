from pytest import mark 
from .conftest import get_client_session
from ..db import (
    User,
    Card,
    Account,
    Transaction,
    AccountTransaction
)

@mark.asyncio
async def test_get_users(get_client_session):
    session = get_client_session
    async with session.get('http://127.0.0.1/api_test/users') as response:
        assert response.status_code == 200