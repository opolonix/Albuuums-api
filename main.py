from typing import Annotated, Optional
from fastapi import Depends, FastAPI
from pydantic import BaseModel


from contextlib import asynccontextmanager

import auth
import users
import albums
import search

@asynccontextmanager
async def main(app: FastAPI):
    yield

app = FastAPI(lifespan=main, root_path="/api")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(albums.router)
app.include_router(search.router)