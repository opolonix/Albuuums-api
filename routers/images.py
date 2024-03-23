import os
import hashlib
from fastapi import Depends, APIRouter, HTTPException
from typing import Annotated
from fastapi import Response, Request
from fastapi import FastAPI, File, UploadFile
import core.schemes as schemes
from core.father import Father
from models import base
from fastapi.responses import FileResponse
from sqlalchemy import or_


father = Father()

router = APIRouter(
    prefix="/files",
    tags=["Файлы (картинки, видео и тд)"]
)

@router.get("/{file_id}")
async def download_file(file_id, response: Response, request: Request) -> schemes.files.File:
    token = request.cookies.get("x-auth-key") if not request.headers.get("x-auth-key") else request.headers.get("x-auth-key")

    try: user: base.User = await father.verify(token=token, request=request, response=response)
    except HTTPException: pass
    
    if user:
        db_file: base.File = father.session.query(base.File).filter(
            or_(base.File.created_by == user.id, base.File.public == True)
        ).first()
        if db_file: return FileResponse(path=f'files/{hex(db_file.id)}', filename=f'{db_file.name}.{db_file.type}', media_type='multipart/form-data')
        else: raise HTTPException(400, "invalid file_id")
    else:
        db_file: base.File = father.session.query(base.File).filter(base.File.public == True).first()
        if db_file: return FileResponse(path=f'files/{hex(db_file.id)}', filename=f'{db_file.name}.{db_file.type}', media_type='multipart/form-data')
        else: raise HTTPException(400, "invalid file_id")



@router.post("/upload")
async def upload_file(public: Annotated[bool, False], file: Annotated[UploadFile, File(...)], response: Response, request: Request) -> schemes.files.File:
    token = request.cookies.get("x-auth-key") if not request.headers.get("x-auth-key") else request.headers.get("x-auth-key")

    try: user: base.User = await father.verify(token=token, request=request, response=response)
    except HTTPException: raise HTTPException(status_code=403, detail="Not authorized")

    f = await file.read()
    file_hash = hashlib.sha256(f).hexdigest()

    db_file: base.File = father.session.query(base.File).filter(base.File.hash == file_hash).first()
    if not db_file:
        name = file.filename.split('.')
        name.pop(-1)
        db_file = base.File(
            hash=file_hash, 
            name='.'.join(name), 
            type=file.filename.split('.')[-1],
            created_by=user.id,
            public=public
        )
        father.session.add(db_file)
        father.session.commit()
        open(f'files/{hex(db_file.id)}', "wb+").write(f)
    return schemes.files.File(id=db_file.id, name=db_file.name, created_at=db_file.created_at, created_by=db_file.created_by, type=db_file.type, public=public)

@router.delete("/drop/{id}")
async def drop_file(id):
    return HTTPException(status_code=200, detail="Successfully deleted")