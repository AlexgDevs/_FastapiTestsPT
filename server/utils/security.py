from os import getenv
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()

schemeO2 = OAuth2PasswordBearer(tokenUrl='/auth/token')

ACCESS_TOKEN_EXP = int(getenv('ACCESS_TOKEN_EXP', 1))
REFRESH_TOKEN_EXP = int(getenv('REFRESH_TOKEN_EXP', 7))
JWT_SECRET = getenv('JWT_SECRET', 'fallback-secret-key')
ALGORITHM = getenv('ALGORITHM', 'HS256')

async def create_access_token(user_data: dict):
    access_exp = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXP)
    payload = {
        'sub': str(user_data.get('id')),
        'user_data': user_data,
        'exp': access_exp, 
        'type': 'access'
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)


async def create_refresh_token(user_data: dict):
    refresh_exp = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXP)
    payload = {
        'sub': str(user_data.get('id')),
        'user_data': user_data, 
        'exp': refresh_exp, 
        'type': 'refresh'
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)


async def verify_token(token: str = Depends(schemeO2)):
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[ALGORITHM],
        )
        return payload.get('user_data')

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized',
            headers={'WWW-Authenticate': 'Bearer'}
        )


async def access_refresh_token(refresh: str):
    payload = jwt.decode(refresh, JWT_SECRET, algorithms=[ALGORITHM])

    if payload.get('type') != 'refresh':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='token type is invalid',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    user_data = payload.get('user_data')
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='user not found',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    return await create_access_token(user_data)


async def get_current_user(token: str = Depends(schemeO2)):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='token is invalid',
            headers={'WWW-Authenticate': 'Bearer'}
        )