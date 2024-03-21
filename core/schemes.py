from typing import Optional
from pydantic import BaseModel

import datetime

class users:

    class User(BaseModel):
        id: int
        username: str
        avatar_id: str | None
        email: str
        name: str
        status: int
        base_album: str

    class signin(BaseModel):
        email: str
        password: str
    
    class signup(BaseModel):
        name: str
        email: str
        password: str
        username: str | None = None

class files:
    class File(BaseModel):
        id: int
        name: str | None = None
        create_from: datetime.datetime
        create_by: int
        file_extension: str
        description: str | None = None

    class Drop(BaseModel):
        album_id: str
        file_id: str
        create_from: datetime.datetime
        create_by: int

class albums:
    class New(BaseModel):
        name: str
        description: str | None = None
        private: bool = True

    class Album(BaseModel):
        id: str
        photos_count: int
        private: bool
        description: str | None = None

        images_count: int
        videos_count: int
        other_count: int