import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import db_manager
from .routers import (
    user_app,
    card_app,
    account_app,
    acc_transaction_app,
    transaction_app,
    auth_app
)

API_URL = 'http://localhost:8000'


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],  # Ваш Flask порт
    allow_credentials=True,  # ОБЯЗАТЕЛЬНО!
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_app)
app.include_router(card_app)
app.include_router(account_app)
app.include_router(acc_transaction_app)
app.include_router(transaction_app)
app.include_router(auth_app)