from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from http import HTTPStatus
from app.db_utils import models, utils
from app.db_utils.database import SessionLocal, engine
from app.routes import schema
from app.routes.utils import hash_pass


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


@router.post("/api/v1/signup/", tags=["signup"], status_code=HTTPStatus.CREATED, response_model=schema.UserOutput)
def create_user(
    user: schema.CreateUser,
    db: Session = Depends(get_db)
):
    """Create a user if not present"""
    db_user = utils.get_user_by_user_id(
        db=db,
        user_id=user.user_id
    )
    if db_user:
        raise HTTPException(status_code=400, detail="Email already present")
    hashed_pass = hash_pass(user.password)
    user.password = hashed_pass
    db_user = utils.create_user(
        db = db,
        user_id = user.user_id,
        username = user.username,
        password = user.password,
        email = user.email
        )
    
    return db_user