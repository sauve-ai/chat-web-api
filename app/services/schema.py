from pydantic import BaseModel
from typing import Optional
import datetime

class CreateUser(BaseModel):
    email: str
    password: str
    username: str

class UserLogin(BaseModel):
    username: str
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

class Token(BaseModel):
    access_token: str
    token_type: str

class URLRequest(BaseModel):
    base_url: str

class chatbotrequest(BaseModel):
    link: str
    query: str