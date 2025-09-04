from . import (
    HTTPException,
    status,
    APIRouter,
    List,
    Depends
)

from ..schemas import (
    UserResponse,
    CreateUserModel,
    PatchUserModel,
    PutUpdateModel,
)

from ..db import (
    Session,
    select,
    User,
    joinedload,
    DBHelper,
    AsyncSession,
    get_session,
    get_session_begin,
    Transaction,
    AccountTransaction,
    Card,
    Account
)

user_app = APIRouter(prefix='/users', tags=['Users'])


@user_app.get('/',
            response_model=List[UserResponse],
            status_code=status.HTTP_200_OK,
            summary='Get all users', description='enpoint for getting all users')
async def get_all_users():
    async with Session() as session:
        users = await session.scalars(
        select(User)
        .options(
            joinedload(User.cards).joinedload(Card.user),
            joinedload(User.accounts).joinedload(Account.cards).joinedload(Card.user),
            joinedload(User.accounts).joinedload(Account.user),
            joinedload(User.account_transactions).joinedload(AccountTransaction.to_account).joinedload(Account.user),
            joinedload(User.account_transactions).joinedload(AccountTransaction.from_account).joinedload(Account.user),
            joinedload(User.account_transactions).joinedload(AccountTransaction.card),
            joinedload(User.account_transactions).joinedload(AccountTransaction.user),
            joinedload(User.transactions).joinedload(Transaction.account).joinedload(Account.user),
            joinedload(User.transactions).joinedload(Transaction.card)
        )
        )
        return users.unique().all()


@user_app.get('/{user_id}',
            response_model=UserResponse,
            summary='Get user by id',
            description='endpoint for getting user by id')
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await session.scalar(
        select(User)
        .where(User.id == user_id)
        .options(
            joinedload(User.cards).joinedload(Card.user),
            joinedload(User.accounts).joinedload(Account.cards).joinedload(Card.user),
            joinedload(User.transactions),
            joinedload(User.account_transactions))
    )

    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User not found'
    )


@user_app.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='Create user',
            description='endpoint for creating user')
async def create_user(user_data: CreateUserModel, session: AsyncSession = Depends(get_session_begin)):
    session.add(User(**user_data.model_dump()))
    return {'status': 'created'}


@user_app.patch('/{user_id}',
                status_code=status.HTTP_200_OK,
                summary='Patch update user',
                description='enpoind for patch update user')
async def patch_update_user(user_id: int, user_data: PatchUserModel, session: AsyncSession = Depends(get_session_begin)):
    user = DBHelper.get_user(user_id)
    if user:
        await session.merge(User(id=user.id, **user_data.model_dump(exclude_unset=True)))
        return {'stauts': 'patch updated'}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User not found'
    )


@user_app.put('/{user_id}',
            status_code=status.HTTP_200_OK,
            summary='Put update user',
            description='endpoint for put update user')
async def put_update_user(user_id: int, user_data: PutUpdateModel, session: AsyncSession = Depends(get_session_begin)):
    user = await DBHelper.get_user(user_id, session)
    if user:
        await session.merge(User(id=user.id, **user_data.model_dump()))
        return {'status': 'put updated'}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User not found'
    )


@user_app.delete('/{user_id}',
                status_code=status.HTTP_200_OK,
                summary='Delete user',
                description='endpoind for deleted user')
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await DBHelper.get_user(user_id)
    if user:
        await session.delete(user)
        return {'status': 'deleted'}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User not found'
    )
