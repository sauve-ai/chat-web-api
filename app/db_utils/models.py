from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.db_utils.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=False, index=True)
    password = Column(String)
 

# class Class(Base):
#     __tablename__='classes'
#     id= Column(Integer,primary_key=True, index=True)
#     name = Column(String(225), index=True)
#     teacher_id = Column(Integer, ForeignKey("teachers.id"))