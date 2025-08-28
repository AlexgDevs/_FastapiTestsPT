from datetime import datetime
from pydantic import BaseModel


class UserAccountResponse(BaseModel):
    id: int
    name: str
    email: str


class AccountResponse(BaseModel):
    id: int
    account_name: str
    balance: int 
    created_at: datetime
    user: UserAccountResponse

    class Config:
        from_attributes = True
