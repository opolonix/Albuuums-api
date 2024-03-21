from functools import lru_cache

from fastapi import FastAPI
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

    async def is_authorized(self, token: str) -> int:
        if not token: return None
        cursor = await self.db.execute(f"SELECT user_id FROM sessions WHERE token = '{token}';")
        session = await cursor.fetchone()
        return int(session[0]) if session else None