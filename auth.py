from typing import Annotated, Optional
from fastapi import Depends, APIRouter
from pydantic import BaseModel

import schemes

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"]
)

@router.post("/signin/LoginPassword")
async def users(
    user: Annotated[schemes.signin.LoginPassword, Depends()]
) -> schemes.User:
    # user = schemes.User(key="228", name="Opolo")
    return {"ok": True}
