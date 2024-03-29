from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.db_utils.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=False, index=True)
    password = Column(String)
 