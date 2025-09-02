from datetime import datetime
from pydantic import BaseModel


class UserAccountResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class AccountResponse(BaseModel):
    id: int
    account_number: str
    account_name: str
    balance: int 
    created_at: datetime
    user: UserAccountResponse

    class Config:
        from_attributes = True


class CreateAccountModel(BaseModel):
    account_name: str
    balance: int
    user_id: int