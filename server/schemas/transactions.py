from datetime import datetime
from typing import Literal
from pydantic import BaseModel

from .card import CardResponse
from .account import AccountResponse


class AccountTransactionResponse(BaseModel):
    id: int
    amount: int
    created_at: datetime
    card: CardResponse
    from_account: AccountResponse
    to_account: AccountResponse

    class Config:
        from_attributes = True


class CreateAccountTransactionModel(BaseModel):
    amount: int
    user_id: int
    card_id: int
    from_account_id: int
    to_account_id: int


class TransactionResponse(BaseModel):
    id: int
    amount: int
    created_at: datetime
    card: CardResponse
    account: AccountResponse
    transaction_type: Literal['from_account', 'to_account']

    class Config:
        from_attributes = True


class CreateTransactionModel(BaseModel):
    amount: int
    card_id: int
    account_id: int
    user_id: int
    transaction_type: Literal['from_account', 'to_account']