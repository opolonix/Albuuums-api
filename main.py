from fastapi import FastAPI
import aiosqlite
from contextlib import asynccontextmanager

from core.father import Father
from core import schemes
from core.config import MYSQLSERVER_URL
from fastapi.middleware.cors import CORSMiddleware

from models.base import Base

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

@asynccontextmanager
async def lifespan(app: FastAPI):

    Father().db = await aiosqlite.connect("data/sessions.db")

    Father().engine = create_engine(MYSQLSERVER_URL)
    Father().sessionmaker = sessionmaker(bind=Father().engine)
    Father().session = Father().sessionmaker()

    Base.metadata.create_all(bind=Father().engine)

    import routers.auth as auth
    import routers.users as users
    import routers.albums as albums
    import routers.images as images

    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(images.router)
    app.include_router(albums.router)

    yield
        
    await Father().db.close()
    Father().sessionmaker.close_all()

app = FastAPI(root_path="/api", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы с любого домена
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

Father().app = app
Father().schemes = schemes

"uvicorn main:app --reload" # в терминал для тестов