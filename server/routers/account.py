from . import (
    APIRouter,
    status,
    HTTPException,
    List,
    Depends
)

from ..db import (
    select,
    Account,
    DBHelper,
    AsyncSession,
    get_session,
    joinedload,
    get_session_begin,
    Card
)

from ..schemas import (
    AccountResponse,
    CreateAccountModel
    )


account_app = APIRouter(prefix='/accounts', tags=['Accounts'])


@account_app.get('/',
                response_model=List[AccountResponse],
                summary='Get all accounts',
                description='endpoint for getting all accounts')
async def get_accounts(session: AsyncSession = Depends(get_session)):
    accounts = await session.scalars(
        select(Account)
        .options(
        joinedload(Account.user),
        joinedload(Account.cards).joinedload(Card.user)
        )
    )

    return accounts.unique().all()


@account_app.get('/{user_id}',
                response_model=List[AccountResponse],
                summary='Get all accounts by user',
                description='endpoint for getting all accounts by user')
async def get_accounts_by_user(user_id: int, session: AsyncSession = Depends(get_session)):
    accounts = await session.scalars(
        select(Account)
        .options(
        joinedload(Account.user),
        joinedload(Account.cards).joinedload(Card.user)
        )
    )
    return accounts.unique().all()


@account_app.get('/{user_id}/{account_id}',
                response_model=AccountResponse,
                summary='Get account by user and account id',
                description='enpoind for getting account by user and account id')
async def get_account_by_user_account_id(user_id: int, account_id: int, session: AsyncSession = Depends(get_session)):
    account = await DBHelper.get_account(user_id, account_id, session)
    if account:
        return account
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Account not found'
    )


@account_app.post('/',
                status_code=status.HTTP_201_CREATED,
                summary='Create account',
                description='endpoind for creating account')
async def create_account(account_data: CreateAccountModel, session: AsyncSession = Depends(get_session_begin)):
    session.add(Account(**account_data.model_dump()))
    return {'status': 'created'}


@account_app.delete('/{user_id}/{account_id}',
                summary='Delete account',
                description='endpoint for deleted account by user and account id')
async def delete_account(user_id: int, account_id: int, session: AsyncSession = Depends(get_session_begin)):
    account = await DBHelper.get_account(user_id, account_id)
    if account:
        await session.delete(account)
        return {'status': 'deleted'}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Account not found'
    )


