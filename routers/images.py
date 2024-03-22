import shutil
from fastapi import Depends, APIRouter, HTTPException
from typing import Annotated
from fastapi import Response, Request
from fastapi import FastAPI, File, UploadFile
import core.schemes as schemes
from core.father import Father
from models import base
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
async def upload_file(file: Annotated[UploadFile, File(...)], response: Response, request: Request) -> schemes.files.File:
    token = request.cookies.get("x-auth-key") if not request.headers.get("x-auth-key") else request.headers.get("x-auth-key")

    try: user: base.User = await father.verify(token=token, request=request, response=response)
    except HTTPException: raise HTTPException(status_code=403, detail="Not authorized")

    with open('files', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return schemes.files.File()

@router.delete("/drop/{id}")
async def drop_file(id):
    return HTTPException(status_code=200, detail="Successfully deleted")