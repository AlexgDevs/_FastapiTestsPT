from datetime import datetime
from pydantic import BaseModel


class CardResponse(BaseModel):
    id: int
    cardholder_name: str  
    card_number: str
    cvv: str 
    expire_date: str  
    created_at: datetime 

    class Config:
        from_attributes = True

