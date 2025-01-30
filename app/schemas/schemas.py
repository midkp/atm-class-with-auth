# app/schemas.py

from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    pin: str

    class Config:
        orm_mode = True
