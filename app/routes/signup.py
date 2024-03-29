from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db_utils import models, utils
from app.db_utils.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router  = APIRouter()

##get database connection
def get_db():
    """Get database connection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/api/v1/signup/", tags=["signup"])
def create_user(
    user_id,
    email,
    password,
    username,
    db: Session = Depends(get_db)
):
    """Create a user from if not present"""
    db_user = utils.get_user_by_user_id(
        db=db,
        user_id=user_id
    )
    if db_user:
        raise HTTPException(status_code=400, detail="Email already present")
    
    ## create a user instance
    db_user = utils.create_user(
        db=db,
        user_id=user_id,
        username=username,
        password=password,
        email=email)
    
    return db_user