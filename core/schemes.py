from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class users:

    class User(BaseModel):
        id: int
        username: str
        avatar_id: int | None
        email: str
        name: str
        status: int
        base_album: int

    class authUser(BaseModel):
        id: int
        cookie: str
        username: str
        avatar_id: int | None
        email: str
        name: str
        status: int
        base_album: int

    class Edit(BaseModel):
        username: str | None = None
        avatar_id: int | None = None
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
        created_at: datetime
        created_by: int
        type: str
        public: bool

    class Drop(BaseModel):
        album_id: int
        file_id: int
        created_from: datetime
        created_by: int

class albums:
    class New(BaseModel):
        name: str
        description: str | None = None
        private: bool = True

    class Pin(BaseModel):
        album_id: int
        file_id: int
        name: str = None
        tags: List[str] = []

    class Album(BaseModel):
        id: int
        album_cover_id: int | None = None
        private: bool = True
        editor: bool = False
        name: str | None = None
        description: str | None = None
    
        tags: List['albums.Tags']
        

    class fullAlbum(BaseModel):
        id: int
        album_cover_id: int | None = None
        private: bool = True
        editor: bool = False
        name: str | None = None
        description: str | None = None
        
        files: List['albums.File']
        tags: List['albums.Tags'] = []

    class Albums(BaseModel):
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