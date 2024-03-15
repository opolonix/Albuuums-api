from fastapi import Depends, APIRouter

import schemes
from auth import verifier
from typing import Optional
router = APIRouter(
    prefix="/albums",
    tags=["Альбомы"]
)

@router.get("/new")
async def users(session_data: schemes.user.Session = Depends(verifier)) -> schemes.albums.Album:
    return session_data

@router.get("/get/self")
async def users(key, session_data: schemes.user.Session = Depends(verifier)) -> list[schemes.albums.Album]:
    return session_data

@router.get("/get/{key}")
async def users(key, session_data: schemes.user.Session = Depends(verifier)) -> schemes.User:
    return session_data

@router.get("/drop/{key}")
async def users(session_data: schemes.user.Session = Depends(verifier)) -> schemes.albums.Album:
    return session_data

@router.get("/add-editor/{key}")
async def users(session_data: schemes.user.Session = Depends(verifier)) -> schemes.albums.Album:
    return session_data

@router.get("/add-viever/{key}")
async def users(session_data: schemes.user.Session = Depends(verifier)) -> schemes.albums.Album:
    return session_data

@router.get("/set-privileges/{key}")
async def users(session_data: schemes.user.Session = Depends(verifier)) -> schemes.albums.Album:
    return session_data