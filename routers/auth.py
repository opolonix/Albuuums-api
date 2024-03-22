from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import text

import hashlib
import core.schemes as schemes
from core.father import Father
from models import base
import re
import secrets
from sqlalchemy import create_engine, and_
from uuid import uuid4
from fastapi import Response, Request

import secrets
import string

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"]
)
father = Father()
db = father.db

@router.get("/signin")
async def signin(user: Annotated[schemes.users.signin, Depends()], response: Response, request: Request) -> schemes.users.User:

    # if not re.fullmatch(r"([a-z0-9._-]+@[a-z0-9._-]+\.[a-z0-9_-]+)", user.email, re.I): # если имейл невалидный то сразу отсекает
    #     raise HTTPException(status_code=403, detail="Аccess is denied")
    token = request.cookies.get("x-auth-key")
    id_auth = await father.is_authorized(token)
    if id_auth:
        user: base.User = Father().session.query(base.User).filter(base.User.id == id_auth).first()
        if user: 
            return schemes.users.User(id=user.id, name=user.name, username=user.username, avatar_id=user.avatar_id, email=user.email, status=user.status, base_album=user.base_album)
        else: response.delete_cookie("x-auth-key")
    elif token: response.delete_cookie("x-auth-key")


    """тут проверка на пользователя"""

    password = hashlib.sha512(bytes(user.password.encode('utf-8'))).hexdigest()

    user: base.User = Father().session.query(base.User).filter(and_(base.User.password == password, base.User.email == user.email)).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Пример получения результатов запроса
    token = secrets.token_hex(32)
    
    await db.execute("INSERT INTO sessions (token, user_id) VALUES (?, ?);", (token, 228))
    await db.commit()

    response.set_cookie(key="x-auth-key", value=token)

    return schemes.users.User(id=user.id, name=user.name, username=user.username, avatar_id=user.avatar_id, email=user.email, status=user.status, base_album=user.base_album)

@router.post("/signup")
async def signup(user: Annotated[schemes.users.signup, Depends()], response: Response, request: Request) -> schemes.users.User:
    
    if not re.fullmatch(r"([a-z0-9._-]+@[a-z0-9._-]+\.[a-z0-9_-]+)", user.email, re.I): # валидация на верно введенный имейл
        raise HTTPException(status_code=400, detail="Invalid email")
    

    if len(user.name) > 16:
        raise HTTPException(status_code=400, detail="Name too long")
    
    if len(user.name) == 0:
        raise HTTPException(status_code=400, detail="Name too short")
    
    if Father().session.query(base.User).filter(base.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="User already exists")
    if user.username:
        if not re.fullmatch(r"([a-z][a-z0-9_]{0,15})", user.username, re.I): # валидация на юзернейм
            raise HTTPException(status_code=400, detail="Username already exists")
        if Father().session.query(base.User).filter(base.User.username == user.username).first():
            raise HTTPException(status_code=400, detail="User already exists")
    else:
        username = str(secrets.choice(string.ascii_letters)) + ''.join(secrets.choice(string.digits) for _ in range(7))
        user.username = str(username)

    token = request.cookies.get("x-auth-key")
    id_auth = await father.is_authorized(token)

    if id_auth:
        fuser: base.User = Father().session.query(base.User).filter(base.User.id == id_auth).first()
        if fuser: 
            return schemes.users.User(id=fuser.id, name=fuser.name, username=fuser.username, avatar_id=fuser.avatar_id, email=fuser.email, status=fuser.status, base_album=fuser.base_album)
        else: response.delete_cookie("x-auth-key")
    elif token: response.delete_cookie("x-auth-key")




    """Генерация пользователя в бд"""

    
    password = hashlib.sha512(bytes(user.password.encode('utf-8'))).hexdigest()
    
    new_user = base.User(
        password = password,
        username = user.username,
        avatar_id = None,
        email = user.email,
        name = user.name,
        status = 0
    )
    Father().session.add(new_user)
    Father().session.commit()

    token = secrets.token_hex(32)

    await db.execute("INSERT INTO sessions (token, user_id) VALUES (?, ?);", (token, new_user.id))
    await db.commit()

    """Создание базового альбома"""

    meta = base.albumsMeta(private=True, created_by=new_user.id, description="Basic album")
    father.session.add(meta)
    father.session.commit()

    access = base.albumsAccess(album_id=meta.id, client_id=new_user.id, editor=True, accessed_by=new_user.id)
    father.session.add(access)
    father.session.commit()

    new_user.base_album = meta.id

    base.get_album(meta.id) # там внутри создаются доп таблицы с файлами и тегами
    base.get_album_tags(meta.id)

    father.session.commit()

    "Установка куки"
    response.set_cookie(key="x-auth-key", value=token)

    return schemes.users.User(id=new_user.id, name=new_user.name, username=new_user.username, avatar_id=new_user.avatar_id, email=new_user.email, status=new_user.status, base_album=new_user.base_album)

@router.get("/logout")
async def logout(response: Response, request: Request):

    if token := request.cookies.get("x-auth-key"): # проверяет существует ли сессия и тогда делает логаут
        await db.execute("DELETE FROM sessions WHERE token = ?;", (token))
        await db.commit()
        response.delete_cookie("x-auth-key")
