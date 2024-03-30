from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

from sqlalchemy.orm import Session

from app.services import utils, create_access_token
from app.routes.signup import get_db
from app.services.schema import Token

routes = APIRouter()

@routes.post("/token")
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
):
    """Get the jwt token for login"""
    user = utils.authenticate_user(
        db= db,
        username=form_data.username,
        password=form_data.password
    )

    if not user:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token.create_access_token(
        data={
             "sub": user.username,
             "pass": user.password
             }, 
             expires_delta=None
    )

    return Token(access_token=access_token, token_type="bearer")