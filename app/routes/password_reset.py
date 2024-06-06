from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from http import HTTPStatus
from app.db_utils import models, utils
from app.db_utils.database import SessionLocal, engine
from app.services.schema import ResetPasswordRequest
from app.services.utils import hash_pass
from pydantic import BaseModel
from typing import Dict
import uuid
from datetime import datetime, timedelta, timezone

models.Base.metadata.create_all(bind=engine)
router  = APIRouter()

def get_db():
    """Get database connection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@router.post("/api/v1/reset_password/", tags=["Reset Password"])
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):

    token_valid_user = utils.is_valid_reset_token(db=db, 
                                 token=request.token)

    if not token_valid_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    hashed_pass = hash_pass(request.new_password)
    print("HASH", hashed_pass)
    print("USER", token_valid_user)
    print("TOKEN", request.token)
    password_reset = utils.reset_password(
        db = db,
        user_id = token_valid_user.user_id,
        hashed_pass = hashed_pass,
        reset_token= request.token
        )
    if password_reset:
        return {"message": "Password has been reset"}
