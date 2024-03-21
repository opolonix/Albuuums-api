from sqlalchemy.orm import DeclarativeBase

# declarative base class
class Base(DeclarativeBase):
    pass

from typing import Optional
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey

from sqlalchemy import Column, Integer, String
from .base import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(128))
    name = Column(String(63))
    username = Column(String(63))
    avatar_id = Column(String(15))
    email = Column(String(63))
    status = Column(Integer)
    base_album = Column(String(15))
