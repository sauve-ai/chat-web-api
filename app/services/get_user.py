from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Annotated

from sqlalchemy.orm import Session

from jose import JWTError, jwt

from app.services import setting
from app.db_utils import utils
from app.routes.signup import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)
        ):
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("create user")
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        user_id: int = int(payload.get("sub"))

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