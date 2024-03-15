from fastapi import Depends, APIRouter

import schemes
from auth import verifier
from typing import Optional

router = APIRouter(
    prefix="/images",
    tags=["Изображение"]
)

@router.get("/get/{key}")
async def users(session_data: schemes.user.Session = Depends(verifier)) -> schemes.albums.Album:
    return session_data

@router.post("/upload")
async def users(session_data: schemes.user.Session = Depends(verifier)) -> schemes.albums.Album:
    return session_data

@router.get("/drop/{key}")
async def users(session_data: schemes.user.Session = Depends(verifier)) -> schemes.albums.Album:
    return session_data