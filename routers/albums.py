from fastapi import Depends, APIRouter

import schemes
from father import Father
father = Father()

router = APIRouter(
    prefix="/albums",
    tags=["Альбомы"]
)

@router.put("/new")
async def new_album(album: schemes.albums.New = Depends()) -> schemes.albums.Album:
    return schemes.albums.Album()

@router.get("/{id}")
async def getting_info(id: str) -> schemes.albums.Album:
    return schemes.albums.Album()

@router.get("/get-files/{id}")
async def getting_files(id: str) -> schemes.albums.Album:
    return schemes.albums.Album()