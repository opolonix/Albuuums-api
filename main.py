from typing import Annotated, Optional
from fastapi import Depends, FastAPI
from pydantic import BaseModel


from contextlib import asynccontextmanager
import auth

@asynccontextmanager
async def main(app: FastAPI):
    yield

app = FastAPI(lifespan=main)
app.include_router(auth.router)
