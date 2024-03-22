from functools import lru_cache

from fastapi import FastAPI, HTTPException
from aiosqlite import Connection
import core.schemes as schemes
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import Session
from fastapi_sessions.frontends.implementations import SessionCookie
from fastapi_sessions.backends.implementations import InMemoryBackend
from sqlalchemy.orm import sessionmaker

@lru_cache(maxsize=1)
class Father:

    

    app: FastAPI
    schemes: schemes
    
    db: Connection
    
    engine: AsyncEngine
    session: Session
    sessionmaker: sessionmaker
    
    def __init__(self) -> None:
        
        from models import base
        self.base: base = base

    async def is_authorized(self, token: str) -> int:
        if not token: return None
        cursor = await self.db.execute(f"SELECT user_id FROM sessions WHERE token = '{token}';")
        session = await cursor.fetchone()
        return int(session[0]) if session else None
    
    async def verify(self, token, request, response):    
        
        token = request.cookies.get("x-auth-key")
        id_auth = await self.is_authorized(token)
        if not id_auth: 
            if token: response.delete_cookie("x-auth-key")
            raise HTTPException(status_code=403, detail="Not authorized")

        user: self.base.User = self.session.query(self.base.User).filter(self.base.User.id == id_auth).first()
        if not user: 
            response.delete_cookie("x-auth-key")
            raise HTTPException(status_code=403, detail="Not authorized")
        
        return user