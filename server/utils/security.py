from os import getenv
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()

schemeO2 = OAuth2PasswordBearer(tokenUrl='/auth/token')

ACCESS_TOKEN_EXP = int(getenv('ACCESS_TOKEN_EXP', 7))
REFRESH_TOKEN_EXP = int(getenv('REFRESH_TOKEN_EXP', 30))
JWT_SECRET = getenv('JWT_SECRET', 'fallback-secret-key')
ALGORITHM = getenv('ALGORITHM', 'HS256')

async def create_access_token(user_data: dict) -> str:
    payload = {
        'sub': str(user_data.get('id')),
        'user_data': user_data,
        'exp': datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXP),
        'type': 'access'
    }
    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=ALGORITHM
    )


async def create_refresh_token(user_data: dict) -> str:
    payload = {
        'sub': str(user_data.get('id')),
        'user_data': user_data,
        'exp': datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXP),
        'type': 'refresh'
    }
    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=ALGORITHM
    )


async def access_refresh_token(refresh: str):
    try:
        payload = jwt.decode(
            refresh,
            JWT_SECRET,
            algorithms=[ALGORITHM]
        )

        if payload.get('type') != 'refresh':
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

        return await create_access_token(payload.get('user_data'))

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(token: str = Depends(schemeO2)):
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[ALGORITHM]
        )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

