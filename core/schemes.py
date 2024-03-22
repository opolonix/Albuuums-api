from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class users:

    class User(BaseModel):
        id: int
        username: str
        avatar_id: str | None
        email: str
        name: str
        status: int
        base_album: str

    class Edit(BaseModel):
        username: str | None = None
        avatar_id: str | None = None
        name: str | None = None

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
        created_from: datetime
        created_by: int
        file_extension: str
        description: str | None = None

    class Drop(BaseModel):
        album_id: str
        file_id: str
        created_from: datetime
        created_by: int

class albums:
    class New(BaseModel):
        name: str
        description: str | None = None
        private: bool = True

    class Album(BaseModel):
        id: str
        album_cover_id: int
        private: bool = True
        editor: bool = False
        description: str | None = None
    
        tags: List['albums.Tags']

    class fullAlbum(BaseModel):
        id: str
        album_cover_id: int
        private: bool = True
        editor: bool = False
        description: str | None = None
        
        files: List['albums.File']
        tags: List['albums.Tags']

    class Albums(BaseModel):
        id: str
        private: bool = True
        description: str | None = None

        images_count: int
        videos_count: int
        other_count: int
        albums: List['albums.Album']

    class Tags(BaseModel):
        tag: str
        file_album_id: int # ссылка на ид файла внутри альбома!

    class File(BaseModel):
        id: int
        file_id: int
        name: str
        type: str
        pinned_at: datetime
        pinned_by: int
        tags: List['albums.Tags']