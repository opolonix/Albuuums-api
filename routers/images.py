from fastapi import Depends, APIRouter, HTTPException
from typing import Annotated

import schemes
from father import Father
father = Father()

router = APIRouter(
    prefix="/files",
    tags=["Файлы (картинки, видео и тд)"]
)

@router.get("/{id}")
async def get_file(id: str) -> schemes.files.File:
    return schemes.files.File()

@router.put("/upload")
async def upload_file() -> schemes.files.File:
    return schemes.files.File()

@router.delete("/drop/{id}")
async def drop_file(id):
    return HTTPException(status_code=200, detail="Successfully deleted")