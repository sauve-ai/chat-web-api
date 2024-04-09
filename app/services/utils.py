from passlib.context import CryptContext
from app.db_utils.database import SessionLocal, engine
from app.db_utils import utils
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(password:str):
    return pwd_context.hash(password)

def verify_password(
        plain_password: str,
        hashed_password: str
):
    """Verify the password with the hashed one"""
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def authenticate_user(
        db,
        username: str,
        password: str
):
    """Authenticate the user based on password ans his hashed password from database"""
    db_user = utils.get_user_by_user_name(
        db=db,
        username=username,
    )
    print(db_user)
    if not db_user:
        return False
    if not verify_password(password, db_user.password):
        return False
    return db_user

class JWTBearer(HTTPBearer):
   async def __call__(self, request: Request):
       credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
       if credentials:
           return credentials.credentials