from pydantic import BaseModel
from typing import Optional
import datetime

class CreateUser(BaseModel):
    user_id: int
    email: str
    password: str
    username: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class DataToken(BaseModel):
    id: Optional[str] = None

class UserOutput(BaseModel):
    user_id: int
    username: str
    class Config:
        orm_mode=True
