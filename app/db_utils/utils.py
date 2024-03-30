from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.db_utils import models

def get_user_by_user_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

##TODO: Make this one
def get_user_by_user_name(db: Session, username: int):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(
        db: Session,
        email: str,
        password: str,
        username: str,
        user_id: int
):
    """Create a user for the signup"""
    ##todo: create a hash for the user
    db_user = models.User(
        email=email,
        user_id=user_id,
        password=password,
        username=username
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user