from fastapi import Depends, APIRouter

import schemes
from auth import verifier
from typing import Optional

router = APIRouter(
    prefix="/search",
    tags=["Поиск"]
)

@router.get("/{input}")
async def users(session_data: schemes.user.Session = Depends(verifier)) -> schemes.albums.Album:
    return session_data

@router.get("/albums/{input}")
async def users(session_data: schemes.user.Session = Depends(verifier)) -> schemes.albums.Album:
    return session_data

@router.get("/images/{input}")
async def users(session_data: schemes.user.Session = Depends(verifier)) -> schemes.albums.Album:
    return session_data

@router.get("/users/{input}")
async def users(session_data: schemes.user.Session = Depends(verifier)) -> schemes.albums.Album:
    return session_data