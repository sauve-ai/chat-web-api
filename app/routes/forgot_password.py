from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from http import HTTPStatus
from app.db_utils import models, utils
from app.db_utils.database import SessionLocal, engine
from app.services.schema import ForgotPasswordRequest 
from pydantic import BaseModel
from typing import Dict
import uuid
from datetime import datetime, timedelta, timezone

models.Base.metadata.create_all(bind=engine)
router  = APIRouter()

reset_tokens: Dict[str, str] = {}

def get_db():
    """Get database connection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/api/v1/forgot_password/", tags=["Forgot Password"])
def forgot_password(request:ForgotPasswordRequest, db: Session = Depends(get_db)):
    email = request.email
    db_user = utils.get_user_by_email(
        db=db,
        email=email
    )
    if not db_user:
        raise HTTPException(status_code=404, detail="Email not registered.")
    else:
        reset_token = str(uuid.uuid4())
        expires_at = datetime.now(timezone.utc)  + timedelta(hours=1)
        print("current time: ", datetime.now(timezone.utc))
        print("Expires at", expires_at)
        utils.create_reset_password_token(
            db= db, 
            user_id= db_user.user_id, 
            reset_token=reset_token, 
            expire_time=expires_at
        )
    # TODO: need to create a mechanism to send an email instead of sending this through HTTP request.
    return {"status":"success",
            "token":reset_token}
    