import asyncio
from aiohttp import ClientSession
from flask import g, redirect, url_for, request
from jose import jwt
from functools import wraps
from os import getenv
from dotenv import load_dotenv

from .. import API_URL

load_dotenv()

JWT_SECRET = getenv('JWT_SECRET')
ALGORITHM = getenv('ALGORITHM')

def auth_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        access_token = request.cookies.get('access_token')
        if access_token:
            try:
                payload = await asyncio.to_thread(
                    jwt.decode, access_token, JWT_SECRET, algorithms=[
                        ALGORITHM]
                )
                g.user = payload.get('user_data')
                return await f(*args, **kwargs)

            except jwt.ExpiredSignatureError:
                return await try_refresh_token(f, *args, **kwargs)
            
            except jwt.InvalidTokenError:
                pass
        return redirect(url_for('login_page'))
    return decorated


def guest_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        access_token = request.cookies.get('access_token')
        if access_token:
            try:
                await asyncio.to_thread(
                    jwt.decode, access_token, JWT_SECRET, algorithms=[
                        ALGORITHM]
                )
                return redirect(url_for('index'))
            except:
                pass
        return await f(*args, **kwargs)

    return decorated


async def try_refresh_token(f, *args, **kwargs):
    refresh_token = request.cookies.get('refresh_token')

    if not refresh_token:
        return redirect(url_for('login_page'))

    try:
        async with ClientSession() as session:
            async with session.post(
                'http://localhost:8000/auth/refresh',
                cookies={'refresh_token': refresh_token}
            ) as response:

                if response.status == 200:
                    data = await response.json()
                    new_access_token = data['new_access_token']

                    response = await f(*args, **kwargs)
                    response.set_cookie(
                        'access_token', new_access_token,
                        httponly=True, secure=False, samesite='Lax'
                    )
                    return response

    except Exception:
        pass

    return redirect(url_for('login_page'))
