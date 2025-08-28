from pytest import mark 
from .conftest import get_client_session

#GET
@mark.asyncio
async def test_all_users(get_client_session):
    async with get_client_session.get('/users') as response:
        assert response.status == 200


@mark.asyncio
async def test_all_cards(get_client_session):
    async with get_client_session.get('/cards') as response:
        assert response.status == 200


@mark.asyncio
async def test_all_accounts(get_client_session):
    async with get_client_session.get('/accounts') as response:
        assert response.status == 200


@mark.asyncio
async def test_all_transactions(get_client_session):
    async with get_client_session.get('/transactions') as response:
        assert response.status == 200


@mark.asyncio
async def test_all_acc_transactions(get_client_session):
    async with get_client_session.get('/account-transactions') as response:
        assert response.status == 200


#POST
@mark.asyncio
async def test_create_user(get_client_session):

    data = {
        'name': 'testUser',
        'password': 'testPassword',
        'email': 'testEmail'
    }

    async with get_client_session.post('/users', json=data) as response:
        assert response.status == 201


@mark.asyncio
async def test_create_account(get_client_session):
    data = {
        'account_name': 'Test Account',
        'balance': 1000,
        'user_id': 1
    }
    async with get_client_session.post('/accounts', json=data) as response:
        assert response.status == 201


@mark.asyncio
async def test_create_card(get_client_session):
    data = {
        'cardholder_name': 'TEST USER',
        'card_number': '1234567812345678',
        'cvv': '123',
        'expire_date': '12/25',
        'created_at': '2024-01-01T00:00:00',
        'user_id': 1,
        'account_id': 1
    }
    async with get_client_session.post('/cards', json=data) as response:
        assert response.status == 201


@mark.asyncio
async def test_create_transaction(get_client_session):
    data = {
        'amount': 500,
        'card_id': 1,
        'account_id': 1,
        'user_id': 1,
        'transaction_type': 'from_account'
    }
    async with get_client_session.post('/transactions', json=data) as response:
        assert response.status == 201


@mark.asyncio
async def test_create_account_transaction(get_client_session):
    data = {
        'amount': 300,
        'user_id': 1,
        'card_id': 1,
        'from_account_id': 1,
        'to_account_id': 2
    }
    async with get_client_session.post('/account-transactions', json=data) as response:
        assert response.status == 201
