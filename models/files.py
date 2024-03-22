from typing import Optional
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy import Integer, String, ForeignKey, BOOLEAN, DateTime
from sqlalchemy import Column, Integer, String
from .base import Base
from datetime import datetime
import pytz

class File(Base):
    __tablename__ = "file"
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    hash = Column(String(128))
    name = Column(String(length=128, collation='utf8mb4_general_ci'))
    type =  Column(String(length=16, collation='utf8mb4_general_ci'))
    
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Moscow')))
    created_by = Column(Integer)