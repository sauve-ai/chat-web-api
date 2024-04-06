from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db_utils.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=False, index=True)
    password = Column(String)
    plan_class = relationship("Plan", back_populates="user")
    fetchurl_class = relationship("FetchUrl", back_populates="user")
 

class Plan(Base):
    __tablename__= 'plan'

    user = relationship("User", back_populates="plan_class")
    plan_name = Column(String(225), index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    plan_id = Column(Integer, index=True)
    message_count = Column(Integer, index=True)
    chatbot_count = Column(Integer, index=True)


class FetchUrl(Base):
    __tablename__ = "fetchurl"

    user = relationship("User", back_populates="fetchurl_class")
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    request = Column(Integer, index=True)
    plan_id = Column(Integer, index=True)


class ChatbotPlan(Base):
    __tablename__ = "chatbotplan"

    user = relationship("User", back_populates="fetchurl_class")
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    request = Column(Integer, index=True)
    plan_id = Column(Integer, index=True)



