from fastapi import FastAPI

from contextlib import asynccontextmanager

from father import Father
import schemes
import aiosqlite

    

@asynccontextmanager
async def main(app: FastAPI):

    open("data/sessions.db","a+").close()

    db = await aiosqlite.connect("data/sessions.db")

    await db.execute("""CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );""")
    
    await db.commit()

    Father().db = db

    import routers.auth as auth
    import routers.users as users
    import routers.albums as albums
    import routers.images as images

    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(images.router)
    app.include_router(albums.router)

    yield

    await db.close()


app = FastAPI(root_path="/api", lifespan=main)
Father().app = app
Father().schemes = schemes