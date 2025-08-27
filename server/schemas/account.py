from datetime import datetime
from pydantic import BaseModel


class AccountResponse(BaseModel):
    id: int
    account_name: str
    balance: int 
    created_at: datetime

    class Config:
        from_attributes = True
