from functools import lru_cache

from fastapi import FastAPI
from aiosqlite import Connection
import schemes

from fastapi_sessions.frontends.implementations import SessionCookie
from fastapi_sessions.backends.implementations import InMemoryBackend

@lru_cache(maxsize=1)
class Father:
    app: FastAPI
    schemes: schemes
    
    db: Connection

    async def is_authorized(self, token: str) -> int:
        print(token)
        cursor = await self.db.execute("SELECT user_id FROM sessions WHERE session_id = ?;", (token))
        session = await cursor.fetchone()
        return int(session[0]) if session else None