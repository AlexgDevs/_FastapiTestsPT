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
    Transaction,
    Account
)

from ..schemas import (
    TransactionResponse,
    CreateTransactionModel
)


transaction_app = APIRouter(prefix='/transactions', tags=['Transactions'])

@transaction_app.get('/',
                        response_model=List[TransactionResponse],
                        summary='Get all transactions',
                        description='enpoind for getting all transactions')
async def get_transactions(session: AsyncSession = Depends(get_session)):
    transactions = await session.scalars(
        select(Transaction)
        .options(
            joinedload(Transaction.account).joinedload(Account.user),
            joinedload(Transaction.card)
        ))

    return transactions.unique().all()


@transaction_app.get('/{user_id}',
                        response_model=List[TransactionResponse],
                        summary='Get all transactions by user',
                        description='enpoind for getting all transactions by user id')
async def get_transactions_by_user(user_id: int, session: AsyncSession = Depends(get_session)):
    transactions = await session.scalars(
        select(Transaction)
        .where(Transaction.user_id == user_id)
        .options(
            joinedload(Transaction.account).joinedload(Account.user),
            joinedload(Transaction.card)
        ))
    return transactions.unique().all()


@transaction_app.post('/',
                        status_code=status.HTTP_201_CREATED,
                        summary='Create transaction',
                        description='endpoint for creating transactions')
async def create_transaction(
    transaction_data: CreateTransactionModel,
    session: AsyncSession = Depends(get_session_begin)):
    session.add(Transaction(**transaction_data.model_dump()))
    return {'status': 'created'}


@transaction_app.delete('/{user_id}/{transaction_id}',
                            summary='Delete transaction',
                            description='endpoint for deleted transactions')
async def delete_transaction(user_id: int, transaction_id: int, session: AsyncSession = Depends(get_session_begin)):
    transaction = await DBHelper.get_transaction(user_id, transaction_id, session)
    if transaction:
        await session.delete(transaction)
        return {'status': 'deleted'}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Transaction not found'
    )