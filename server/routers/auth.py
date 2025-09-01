from fastapi import Body, Response, Cookie
from passlib.context import CryptContext

from . import (
    APIRouter,
    status,
    HTTPException,
    List,
    Depends,
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
    CreateUserModel,
    LoginUserModel
)

from ..utils import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    jwt,
    JWT_SECRET,
    ALGORITHM
)

from jose import JWTError

auth_app = APIRouter(prefix='/auth', tags=['Auth'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@auth_app.post('/register',
            status_code=status.HTTP_201_CREATED,
            summary='Create user',
            description='endpoint for creating user')
async def create_user(
    response: Response,
    user_data: CreateUserModel, 
    session: AsyncSession = Depends(get_session_begin)
    ):
    password_hash = pwd_context.hash(user_data.password)
    user_dict = user_data.model_dump()
    user_dict['password'] = password_hash
    new_user = User(**user_dict)
    session.add(new_user)
    await session.flush()
    sub_data = {'id': new_user.id, 'name': new_user.name}

    access_token = await create_access_token(sub_data)
    refresh_token = await create_refresh_token(sub_data)

    response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=604800,
            path="/"
        )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax", 
        max_age=2592000,
        path="/auth/refresh"
    )

    return {'status': 'created',
            'tokens': {
                'access': access_token,
                'refresh': refresh_token
                }}


@auth_app.post('/token',
            summary='Get tokens by user registered',
            description='endpoind for getting tokens by user authorisations')
async def login_user(
    response: Response,
    user_form: LoginUserModel, 
    session: AsyncSession = Depends(get_session),
    ):
    try:
        user = await session.scalar(
            select(User)
            .where(User.name == user_form.name)
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
        access_token = await create_access_token(sub_data)
        refresh_token = await create_refresh_token(sub_data)
        
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=604800,
            path="/"
        )
        
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax", 
            max_age=2592000,
            path="/auth/refresh"
        )

        return {
            'tokens': 
            {'acces': access_token, 
            'refresh': refresh_token}}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized',
            headers={'WWW-Authenticate': 'Bearer'}
        )


@auth_app.post('/refresh',
            summary='refresh access token',
            description='endpoint for refreshing access token')
async def update_refresh_token(response: Response, refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="token missing")
    
    payload = jwt.decode(
        refresh_token,
        JWT_SECRET,
        algorithms=[ALGORITHM]
    )

    if payload.get('type') != 'refresh':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid type token',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    new_access_token = await create_access_token(payload.get('user_data'))
    response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=604800,
            path="/"
        )

    return {'new_access_token': new_access_token}