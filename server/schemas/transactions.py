from datetime import datetime
from typing import Literal
from pydantic import BaseModel

from .card import CardResponse
from .user import UserResponse
from .account import AccountResponse


class TransactionResponse(BaseModel):
    id: int
    amount: int
    created_at: datetime
    card: CardResponse
    account: AccountResponse
    user: UserResponse
    transaction_type: Literal['from_account', 'to_account']


class AccountTransactionResponse(BaseModel):
    id: int
    amount: int
    created_at: datetime
    card: CardResponse
    from_account: AccountResponse
    to_account: AccountResponse

    class Config:
        from_attributes = True
