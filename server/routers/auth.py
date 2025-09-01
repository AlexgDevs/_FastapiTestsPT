from fastapi import Body
from passlib.context import CryptContext

from . import (
    APIRouter,
    status,
    HTTPException,
    List,
    Depends,
    OAuth2PasswordRequestForm
)

from ..db import (
    select,
    DBHelper,
    AsyncSession,
    get_session,
    joinedload,
    get_session_begin,
    User
)

from ..schemas import (
    CreateUserModel
)

from ..utils import (
    create_access_token,
    create_refresh_token,
    verify_token,
    get_current_user,
    JWTError
)

auth_app = APIRouter(prefix='/auth', tags=['Auth'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@auth_app.post('/register',
            status_code=status.HTTP_201_CREATED,
            summary='Create user',
            description='endpoint for creating user')
async def create_user(user_data: CreateUserModel, session: AsyncSession = Depends(get_session_begin)):
    password_hash = pwd_context.hash(user_data.password)
    user_dict = user_data.model_dump()
    user_dict['password'] = password_hash
    new_user = User(**user_dict)
    session.add(new_user)
    await session.flush()
    sub_data = {'id': new_user.id, 'name': new_user.name}

    return {'status': 'created',
            'tokens': {
                'access': await create_access_token(sub_data),
                'refresh': await create_refresh_token(sub_data)
                }}


@auth_app.post('/token',
            summary='Get tokens by user registered',
            description='endpoind for getting tokens by user authorisations')
async def login_user(user_form: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    try:
        user = await session.scalar(
            select(User)
            .where(User.name == user_form.username)
        )

        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

        if not pwd_context.verify(user_form.password, user.password):
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Password invalid',
        )

        sub_data = {'id': user.id, 'name': user.name}
        return {
            'tokens': 
            {'acces': await create_access_token(sub_data), 
            'refresh': await create_refresh_token(sub_data)}}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized',
            headers={'WWW-Authenticate': 'Bearer'}
        )


@auth_app.post('/refresh',
            summary='refresh access token',
            description='endpoint for refreshing access token')
async def refresh_token(token: str = Body(..., embed=True)):
    pass 