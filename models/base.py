from sqlalchemy.orm import DeclarativeBase

# declarative base class
class Base(DeclarativeBase):
    pass

from .users import User
from .albums import albumsAccess, albumsMeta, get_album, get_album_tags