from typing import Optional
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey

from sqlalchemy import Column, Integer, String
from .base import Base

class User(Base):
    __tablename__ = "user"
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(128))
    name = Column(String(length=128, collation='utf8mb4_general_ci'))
    username = Column(String(63))
    avatar_id = Column(Integer)
    email = Column(String(63))
    status = Column(Integer)
    base_album = Column(Integer)