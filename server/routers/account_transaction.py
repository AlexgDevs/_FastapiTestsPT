from . import (
    APIRouter,
    status,
    HTTPException,
    List,
    Depends
)

from ..db import (
    select,
    Card,
    DBHelper,
    AsyncSession,
    get_session,
    joinedload,
    get_session_begin,
    AccountTransaction,
    Account
)

from ..schemas import (
    AccountTransactionResponse,
    CreateAccountTransactionModel,
)

acc_transaction_app = APIRouter(
    prefix='/account-transactions', tags=['Account Transactions'])


@acc_transaction_app.get('/',
                        response_model=List[AccountTransactionResponse],
                        summary='Get all account transactions',
                        description='enpoind for getting all account transactions')
async def get_account_transactions(session: AsyncSession = Depends(get_session)):
    acc_transactions = await session.scalars(
        select(AccountTransaction)
        .options(
            joinedload(AccountTransaction.to_account).joinedload(Account.user),
            joinedload(AccountTransaction.from_account).joinedload(Account.user),
            joinedload(AccountTransaction.card).joinedload(Card.user)
        ))

    return acc_transactions.unique().all()


@acc_transaction_app.get('/{user_id}',
                        response_model=List[AccountTransactionResponse],
                        summary='Get all account transactions by user',
                        description='enpoind for getting all account transactions by user id')
async def get_account_transactions_by_user(user_id: int, session: AsyncSession = Depends(get_session)):
    acc_transactions = await session.scalars(
        select(AccountTransaction)
        .where(AccountTransaction.user_id == user_id)
        .options(
            joinedload(AccountTransaction.to_account).joinedload(Account.user),
            joinedload(AccountTransaction.from_account).joinedload(Account.user),
            joinedload(AccountTransaction.card).joinedload(Card.user)
        ))

    return acc_transactions.unique().all()


@acc_transaction_app.post('/',
                        status_code=status.HTTP_201_CREATED,
                        summary='Create Account transaction',
                        description='endpoint for creating acc transactions')
async def create_acc_transaction(
    transaction_data: CreateAccountTransactionModel,
    session: AsyncSession = Depends(get_session_begin)):
    session.add(AccountTransaction(**transaction_data.model_dump()))
    return {'status': 'created'}


@acc_transaction_app.delete('/{user_id}/{transaction_id}',
                            summary='Delete transaction',
                            description='endpoint for deleted acc transactions')
async def delete_transaction(user_id: int, transaction_id: int, session: AsyncSession = Depends(get_session_begin)):
    acc_transaction = await DBHelper.get_acc_transaction(user_id, transaction_id)
    if acc_transaction:
        await session.delete(acc_transaction)
        return {'status': 'deleted'}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Account Transaction not found'
    )
