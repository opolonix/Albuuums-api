from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    key: str
    name: str

class user:
    class Session(BaseModel):
        username: str
    
class signin:
    class LoginPassword(BaseModel):
        login: str
        password: str

class signup:
    class LoginPassword(BaseModel):
        login: str
        password: str
        key: str
        first_name: str
        last_name: Optional[str | None] = None

class albums:
    class Album(BaseModel):
        key: str
        photos_count: int
        
    class NewAlbum(BaseModel):
        name: str
        private: bool = True