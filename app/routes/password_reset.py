from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from http import HTTPStatus
from app.db_utils import models, utils
from app.db_utils.database import SessionLocal, engine
from app.db_utils.models import PasswordResetToken
from app.services import schema
from app.services.utils import hash_pass
from pydantic import BaseModel
from typing import Dict
import uuid
from datetime import datetime, timedelta, timezone


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    
@app.post("/reset-password/")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    email = request.email
    db_user = utils.get_user_by_email(
        db=db,
        email=email
    )
    reset_token = db.query(PasswordResetToken).filter(PasswordResetToken.token == request.token).first()
    if not reset_token or reset_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == reset_token.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = bcrypt.hashpw(request.new_password.encode('utf-8'), bcrypt.gensalt())
    user.hashed_password = hashed_password.decode('utf-8')
    db.commit()

    db.delete(reset_token)
    db.commit()

    return {"message": "Password has been reset"}
