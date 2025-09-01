from datetime import datetime
from typing import List, Literal
from pydantic import BaseModel

from .card import CardResponse
from .account import AccountResponse
from .transactions import TransactionResponse, AccountTransactionResponse


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    cards: List[CardResponse]
    accounts: List[AccountResponse]
    transactions: List[TransactionResponse]
    account_transactions: List[AccountTransactionResponse]

    class Config:
        from_attributes = True


class CreateUserModel(BaseModel):
    name: str
    password: str
    email: str


class LoginUserModel(BaseModel):
    name: str
    password: str

class PatchUserModel(BaseModel):
    name: str | None = None
    password: str | None = None
    email: str | None = None


class PutUpdateModel(BaseModel):
    name: str
    password: str
    email: str

