from fastapi import Depends, APIRouter

import core.schemes as schemes
from core.father import Father
father = Father()

router = APIRouter(
    prefix="/albums",
    tags=["Альбомы"]
)

@router.post("/new")
async def new_album(album: schemes.albums.New = Depends()) -> schemes.albums.fullAlbum:
    return schemes.albums.fullAlbum()

@router.get("/{id}")
async def getting_info(id: str) -> schemes.albums.fullAlbum:
    return schemes.albums.fullAlbum()

@router.get("/get-my-albums")
async def getting_your_albums(id: str) -> schemes.albums.Albums:
    return schemes.albums.Album()