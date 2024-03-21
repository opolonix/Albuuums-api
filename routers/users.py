from fastapi import Depends, APIRouter, Request, HTTPException, Response

import core.schemes as schemes

from core.father import Father
from models import base
father = Father()

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)

@router.get("/get-me")
async def get_yourself(request: Request, response: Response):
    token = request.cookies.get("x-auth-key")
    id_auth = await father.is_authorized(token)
    if id_auth:
        user: base.User = Father().session.query(base.User).filter(base.User.id == id_auth).first()
        if user: 
            return schemes.users.User(id=user.id, name=user.name, username=user.username, avatar_id=user.avatar_id, email=user.email, status=user.status, base_album=user.base_album)
        else: response.delete_cookie("x-auth-key")
    elif token: response.delete_cookie("x-auth-key")
    raise HTTPException(status_code=403, detail="Not authorized")

@router.get("/get/{username}")
async def get_user(username, request: Request) -> schemes.users.User:
    return schemes.users.User(key="228", name="228")

