from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

from sqlalchemy.orm import Session

from app.services import utils, create_access_token, setting
from app.routes.signup import get_db
from app.services.schema import Token,UserLogin

from datetime import datetime, timedelta, timezone


routes = APIRouter()

@routes.post("/api/v1/token")
def login_for_access_token(
        login_data: UserLogin,
        db: Session = Depends(get_db)
):
    """Get the jwt token for login"""
    user = utils.authenticate_user(
        db= db,
        username=login_data.username,
        password=login_data.password
    )

    if not user:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token.create_access_token(
        data={
             "sub": str(user.user_id),
             }, 
             expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")