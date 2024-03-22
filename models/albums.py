from typing import Optional
from core.father import Father
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, BOOLEAN, DateTime
from datetime import datetime
from sqlalchemy import Column, Integer, String
from .base import Base
import pytz

def get_album(album_id: int):
    class Album(Base):
        __tablename__ = f"albumFiles_{album_id}"
        __table_args__ = {'extend_existing': True}

        id = Column(Integer, primary_key=True, autoincrement=True)
        file_id = Column(Integer)
        name = Column(String(128), default=None)
        type = Column(String(16))
        pinned_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Moscow')))
        pinned_by = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))

    Album.metadata.create_all(bind=Father().engine)
    return Album

def get_album_tags(album_id: int):
    class AlbumTags(Base):
        __tablename__ = f"albumTags_{album_id}"
        __table_args__ = {'extend_existing': True}

        id = Column(Integer, primary_key=True, autoincrement=True)
        file_album_id = Column(Integer, ForeignKey(f'albumFiles_{album_id}.id', ondelete='CASCADE'), comment="Не конкретно файл айди, а айди записи внутри альбома для этого файла")
        tag = Column(String(64))

        added_at = Column(DateTime, default=datetime.now(pytz.timezone('Europe/Moscow')))
        added_by = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))


    AlbumTags.metadata.create_all(bind=Father().engine)
    return AlbumTags

class albumsAccess(Base):
    __tablename__ = f"albumsAccess"

    id = Column(Integer, primary_key=True, autoincrement=True)
    album_id: int = Column(Integer)
    client_id: int = Column(Integer)
    editor: bool = Column(BOOLEAN, default=False)
    viewer: bool = Column(BOOLEAN, default=True)
    created_at = Column(DateTime, default=datetime.now(pytz.timezone('Europe/Moscow')))
    accessed_by = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))

class albumsMeta(Base):
    __tablename__ = f"albumsMeta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    private: bool = Column(BOOLEAN, default=True)
    created_at: datetime = Column(DateTime, default=datetime.now(pytz.timezone('Europe/Moscow')))
    created_by = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    name = Column(String(128))
    description = Column(String(512), default=None)