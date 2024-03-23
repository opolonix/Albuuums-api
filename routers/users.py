from fastapi import Depends, APIRouter, Request, HTTPException, Response
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import text

import core.schemes as schemes
import re
from core.father import Father
from models import base
father = Father()

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)

@router.get("/get-me")
async def get_yourself(request: Request, response: Response) -> schemes.users.User:
    token = request.cookies.get("x-auth-key") if not request.headers.get("x-auth-key") else request.headers.get("x-auth-key")
    
    try: user: base.User = await father.verify(token=token, request=request, response=response)
    except HTTPException: raise HTTPException(status_code=403, detail="Not authorized")

    return schemes.users.User(id=user.id, name=user.name, username=user.username, avatar_id=user.avatar_id, email=user.email, status=user.status, base_album=user.base_album)


@router.get("/edit-me")
async def edit_personal_data(data: Annotated[schemes.users.Edit, Depends()], request: Request, response: Response) -> schemes.users.User:
    token = request.cookies.get("x-auth-key") if not request.headers.get("x-auth-key") else request.headers.get("x-auth-key")
    
    try: user: base.User = await father.verify(token=token, request=request, response=response)
    except HTTPException: raise HTTPException(status_code=403, detail="Not authorized")

    if data.avatar_id: user.avatar_id = data.avatar_id
    if data.username: 
        if not re.fullmatch(r"([a-z][a-z0-9_]{0,15})", data.username, re.I): # валидация на юзернейм
            raise HTTPException(status_code=400, detail="Username is invalid")
        if Father().session.query(base.User).filter(base.User.username == data.username).first():
            raise HTTPException(status_code=400, detail="Username already exists")
        user.username = data.username
    if data.name:
        if len(user.name) > 16:
            raise HTTPException(status_code=400, detail="Name too long")
        if len(user.name) == 0:
            raise HTTPException(status_code=400, detail="Name too short")
        user.name = data.name

    Father().session.commit()

    return schemes.users.User(id=user.id, name=user.name, username=user.username, avatar_id=user.avatar_id, email=user.email, status=user.status, base_album=user.base_album)

@router.get("/get/{username}")
async def get_user(username, request: Request, response: Response) -> schemes.users.User:
    user: base.User = Father().session.query(base.User).filter(base.User.username == username).first()
    if user: 
        return schemes.users.User(id=user.id, name=user.name, username=user.username, avatar_id=user.avatar_id, email=user.email, status=user.status, base_album=user.base_album)
    raise HTTPException(status_code=400, detail="Username does not exist")

