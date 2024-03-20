from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException

import schemes
from father import Father
import re
import secrets

from uuid import uuid4
from fastapi import Response, Request

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

    if token := request.cookies.get("x-auth-key"): # не дает спамить созданием сессий 
        if user_id := father.is_authorized(token): # возвращает уже существующего пользователя согласно иду в сессии
            return user_id
        else: 
            response.delete_cookie("x-auth-key")


    """тут проверка на пользователя... должна быть"""


    token = secrets.token_hex(32)
    
    await db.execute("INSERT INTO sessions (session_id, user_id) VALUES (?, ?);", (token, 228))
    await db.commit()

    response.set_cookie(key="x-auth-key", value=token)

    return schemes.users.User()

@router.post("/signup")
async def signup(user: Annotated[schemes.users.signup, Depends()], response: Response, request: Request) -> schemes.users.User:
    
    if not re.fullmatch(r"([a-z0-9._-]+@[a-z0-9._-]+\.[a-z0-9_-]+)", user.email, re.I): # валидация на верно введенный имейл
        raise HTTPException(status_code=400, detail="Invalid email")
    
    if not re.fullmatch(r"([a-z][a-z0-9_]{0,15})", user.username, re.I): # валидация на юзернейм
        raise HTTPException(status_code=400, detail="Invalid username")

    if token := request.cookies.get("x-auth-key"): # не дает спамить созданием сессий 
        if user_id := father.is_authorized(token): # возвращает уже существующего пользователя согласно иду в сессии
            return user_id
        else: 
            response.delete_cookie("x-auth-key")


    """Генерация пользователя в бд"""


    token = secrets.token_hex(32)

    await db.execute("INSERT INTO sessions (session_id, user_id) VALUES (?, ?);", (token, 228))
    await db.commit()

    response.set_cookie(key="x-auth-key", value=token)

    return schemes.users.User()

@router.get("/logout")
async def logout(response: Response, request: Request):

    if token := request.cookies.get("x-auth-key"): # проверяет существует ли сессия и тогда делает логаут
        await db.execute("DELETE FROM sessions WHERE session_id = ?;", (token))
        await db.commit()
        response.delete_cookie("x-auth-key")
