from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    password: str
    email: str

    class Config:
        from_attributes = True