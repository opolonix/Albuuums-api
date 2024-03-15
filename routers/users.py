from fastapi import Depends, APIRouter

import schemes
from routers.auth import verifier

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)

@router.get("/get/self")
async def users(session_data: schemes.user.Session = Depends(verifier)) -> schemes.User:
    return session_data

@router.get("/get/{key}")
async def users(key, session_data: schemes.user.Session = Depends(verifier)) -> schemes.User:
    return session_data