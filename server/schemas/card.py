from datetime import datetime
from pydantic import BaseModel


class UserCardResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class CardResponse(BaseModel):
    id: int
    cardholder_name: str  
    card_number: str
    cvv: str 
    expire_date: str  
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True


class CreateCardModel(BaseModel):
    cardholder_name: str  
    card_number: str
    cvv: str 
    expire_date: str  
    created_at: datetime
    user_id: int
    account_id: int
