from fastapi import Depends, APIRouter

import schemes
from routers.auth import verifier

router = APIRouter(
    prefix="/tags",
    tags=["Теги"]
)

@router.get("/get/random")
async def users(session_data: schemes.user.Session = Depends(verifier)) -> schemes.User:
    return session_data

@router.get("/get/random/{count}")
async def users(count, session_data: schemes.user.Session = Depends(verifier)) -> schemes.User:
    return session_data

@router.get("/get/similar/{input}")
async def users(input, session_data: schemes.user.Session = Depends(verifier)) -> schemes.User:
    return session_data