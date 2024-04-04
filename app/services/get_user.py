from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials

from typing import Annotated

from sqlalchemy.orm import Session

from jose import JWTError, jwt

from app.services import setting
from app.db_utils import utils

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
        credentials: str,
        db
        ):
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("create user")
        payload = jwt.decode(credentials, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        user_id: int = int(payload.get("sub"))
        print(user_id)
        if user_id is None:
            raise credentials_exception
        
        ##TODO: Validate the user password

        token_data_username = user_id

    except Exception as e:
        print(e)
        raise credentials_exception
    user = utils.get_user_by_user_id(db=db, user_id=user_id)
    
    if user is None:
        raise credentials_exception
    return user