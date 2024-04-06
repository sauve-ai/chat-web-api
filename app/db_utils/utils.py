from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.db_utils import models

def get_user_by_user_id(db, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

##TODO: Make this one
def get_user_by_user_name(db, username: int):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db, email: int):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_userid_request_table(db, user_id:int):
    return db.query(models.FetchUrl).filter(models.FetchUrl.user_id == user_id).first()
    

def create_user(
        db: Session,
        email: str,
        password: str,
        username: str,
):
    """Create a user for the signup"""
    ##todo: create a hash for the user
    db_user = models.User(
        email=email,
        password=password,
        username=username
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def create_user_plan(
        db: Session,
        user_id: int,
        plan_id: int,
        plan_name: str,
        messages_count: int,
        chatbot_count: int
):
    """Create a user for the signup"""
    ##todo: create a hash for the user
    db_user_plan = models.Plan(
        user_id=user_id,
        messages_count=messages_count,
        chatbot_count=chatbot_count,
        plan_name= plan_name,
        plan_id = plan_id
    )

    db.add(db_user_plan)
    db.commit()
    db.refresh(db_user_plan)
    
    return db_user_plan


def create_user_plan_request(
        db: Session,
        user_id: int,
        request: int,
        plan_id: int
):
    """Create a user for the signup"""
    ##todo: create a hash for the user
    db_user_plan_request = models.FetchUrl(
        user_id=user_id,
        request= request,
        plan_id = plan_id
    )

    db.add(db_user_plan_request)
    db.commit()
    db.refresh(db_user_plan_request)
    
    return db_user_plan_request