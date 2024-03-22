from fastapi import Depends, APIRouter, HTTPException
from typing import Annotated

import core.schemes as schemes
from core.father import Father
father = Father()

router = APIRouter(
    prefix="/files",
    tags=["Файлы (картинки, видео и тд)"]
)

@router.get("/{file_id}")
async def get_file(id: str) -> schemes.files.File:
    return schemes.files.File()

@router.get("/album/{album_id}/id/{file_id}")
async def get_file_from_album(album_id: int, file_id: int) -> schemes.files.File:
    return schemes.files.File()

@router.post("/upload")
async def upload_file() -> schemes.files.File:
    return schemes.files.File()

@router.delete("/drop/{id}")
async def drop_file(id):
    return HTTPException(status_code=200, detail="Successfully deleted")