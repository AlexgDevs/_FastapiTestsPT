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


class TransactionResponse(BaseModel):
    id: int
    amount: int
    created_at: datetime
    card: CardResponse
    account: AccountResponse
    transaction_type: Literal['from_account', 'to_account']