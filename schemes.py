from pydantic import BaseModel

class User(BaseModel):
    key: str
    name: str
    
class signin:
    class LoginPassword(BaseModel):
        login: str
        password: str