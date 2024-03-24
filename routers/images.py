import os
import hashlib
from fastapi import Depends, APIRouter, HTTPException
from typing import Annotated, List, Optional
from fastapi import Response, Request
from fastapi import FastAPI, File, UploadFile
import core.schemes as schemes
from core.father import Father
from models import base
from fastapi.responses import FileResponse
from sqlalchemy import or_, and_
from urllib.parse import quote
import re

import io
import zipfile

father = Father()

router = APIRouter(
    prefix="/files",
    tags=["Файлы (картинки, видео и тд)"]
)
from fastapi.responses import StreamingResponse

@router.get("/{file_id}")
async def view_file(file_id: int, response: Response, request: Request) -> schemes.files.File:
    token = request.cookies.get("x-auth-key") if not request.headers.get("x-auth-key") else request.headers.get("x-auth-key")

    try: user: base.User = await father.verify(token=token, request=request, response=response)
    except HTTPException: user = None

    if not os.path.exists(f'files/{hex(file_id)}'): raise HTTPException(400, "invalid file_id")

    if user:
        db_file: base.File = father.session.query(base.File).filter(
            and_(
                or_(base.File.created_by == user.id, base.File.public == True),
                base.File.id == file_id
            )
            
        ).first()
    else:
        db_file: base.File = father.session.query(base.File).filter(base.File.public == True, base.File.id == file_id).first()

    if db_file:
        file_type = db_file.type.lower()
        filename = quote(f'{db_file.name}.{db_file.type}')
        media_type = (
            'image/jpeg' if file_type in ['jpg', 'jpeg']
            else 'image/png' if file_type == 'png'
            else 'video/mp4' if file_type == 'mp4'
            else 'video/quicktime' if file_type in ['mov', 'qt']
            else 'image/gif' if file_type == 'gif'
            else 'image/bmp' if file_type in ['bmp', 'dib']
            else 'image/webp' if file_type == 'webp'
            else 'image/tiff' if file_type in ['tiff', 'tif']
            else 'image/x-icon' if file_type == 'ico'
            else 'image/svg+xml' if file_type in ['svg', 'svgz']
            else 'video/webm' if file_type == 'webm'
            else 'video/ogg' if file_type == 'ogg'
            else 'video/avi' if file_type == 'avi'
            else 'application/pdf' if file_type == 'pdf'
            else 'application/octet-stream'  # Общий тип для остальных файлов
        )
            
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        response.headers["Content-Type"] = media_type
    
        return StreamingResponse(open(f"files/{hex(file_id)}", "rb"), media_type=media_type)
        # return StreamingResponse(open(f'files/{hex(file_id)}', "rb"), media_type=media_type)
    else:
        raise HTTPException(400, "invalid file_id")
@router.post("/download-files")
async def download_files(
        response: Response, request: Request, 
        files_ids: List[int]
    ):
    memory_zip = io.BytesIO()
    in_zip = []
    records = father.session.query(base.File).filter(base.File.id.in_(files_ids)).all()
    with zipfile.ZipFile(memory_zip, 'w') as zipf:
        for file in records:
            if os.path.exists(f'files/{hex(file.id)}') and file.id not in in_zip:
            # Добавление файла в архив
                in_zip.append(file.id)
                zipf.write(f'files/{hex(file.id)}', arcname=f'{file.name}.{file.type}')
    memory_zip.seek(0)
    
    # Отправка архива клиенту как потокового ответа
    return StreamingResponse(iter([memory_zip.getvalue()]), media_type="application/zip", headers={"Content-Disposition": f"attachment; filename=FILES.zip"})

@router.get("/download-album/{album_id}")
async def download_album(
        album_id: int,
        response: Response, request: Request, 
    ):

    token = request.cookies.get("x-auth-key") if not request.headers.get("x-auth-key") else request.headers.get("x-auth-key")
    try: user: base.User = await father.verify(token=token, request=request, response=response)
    except HTTPException: user = None

    meta: base.albumsMeta = father.session.query(base.albumsMeta).filter(base.albumsMeta.id == album_id).first()
    if not meta: raise HTTPException(400, "invalid album_id")
    if not meta.private or user:
        album_access: base.albumsAccess = father.session.query(base.albumsAccess).filter(base.albumsAccess.client_id == user.id, base.albumsAccess.album_id == album_id).first()
        if album_access:
            files_meta = father.session.query(base.get_album(album_id)).all()
            memory_zip = io.BytesIO()
            in_zip = []
            with zipfile.ZipFile(memory_zip, 'w') as zipf:
                for file_meta in files_meta:
                    if os.path.exists(f'files/{hex(file_meta.file_id)}') and file_meta.file_id not in in_zip:
                    # Добавление файла в архив
                        in_zip.append(file_meta.file_id)
                        zipf.write(f'files/{hex(file_meta.file_id)}', arcname=f'{file_meta.name}.{file_meta.type}')
            memory_zip.seek(0)
            
            # Отправка архива клиенту как потокового ответа
            return StreamingResponse(iter([memory_zip.getvalue()]), media_type="application/zip", headers={"Content-Disposition": f"attachment; filename=ALBUM{album_id}.zip"})
    
    raise HTTPException(status_code=400, detail="There is no access or the album does not exist")

@router.post("/upload")
async def upload_file(
        public: Annotated[bool, False], 
        file: Annotated[UploadFile, File(...)], 
        response: Response, request: Request, 
        pin_to: Optional[int] = None, 
        tags: List[str] = []
    ) -> schemes.files.File:
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
    else:
        if public: 
            db_file.public = True
            father.session.commit()

    album_id = pin_to if pin_to else user.base_album
    if not father.session.query(base.albumsMeta).filter(base.albumsMeta.id == album_id).first():
        album_id = user.base_album
    albums_id = [album_id] if album_id == user.base_album else [album_id, user.base_album]

    if not os.path.exists(f'files/{hex(db_file.id)}'): open(f'files/{hex(db_file.id)}', "wb+").write(f)

    """Прикрепление файла в альбом, добавляется в pin_to и в родительский"""
    for album_id in albums_id:
        new_pin = base.get_album(album_id)(file_id=db_file.id, name=db_file.name, type=db_file.type, pinned_by=user.id)
        father.session.add(new_pin)
        father.session.commit()

        tag = base.get_album_tags(album_id)
        tags = list(set([i for i in tags if re.fullmatch(r'[a-zа-я\-\_\*\+\.]{1,16}', i, re.I)]))
        for t in tags:
            father.session.add(tag(file_album_id=new_pin.id, tag=t, added_by=user.id))
        father.session.commit()


    return schemes.files.File(id=db_file.id, name=db_file.name, created_at=db_file.created_at, created_by=db_file.created_by, type=db_file.type, public=public)

# @router.post("/pin")
# async def upload_file(
#         pin_to: int,
#         file_id: int,
#         response: Response, request: Request, 
#         tags: List[str] = []
#     ) -> schemes.files.File:
#     token = request.cookies.get("x-auth-key") if not request.headers.get("x-auth-key") else request.headers.get("x-auth-key")

#     try: user: base.User = await father.verify(token=token, request=request, response=response)
#     except HTTPException: raise HTTPException(status_code=403, detail="Not authorized")

#     db_file: base.File = father.session.query(base.File).filter(base.File.id == file_id).first()
#     if not db_file:
#         raise HTTPException(status_code=400, detail="The file does not exist")
#     elif not os.path.exists(f'files/{hex(db_file.id)}'):
#         raise HTTPException(status_code=400, detail="The file does not exist")

#     # добавить проверку прав доступа на просмотр файла

#     if not father.session.query(base.albumsMeta).filter(base.albumsMeta.id == pin_to).first():
#         raise HTTPException(status_code=400, detail="The album does not exist")

#     """Прикрепление файла в альбом, добавляется в pin_to и в родительский"""

#     new_pin = base.get_album(pin_to)(file_id=db_file.id, name=db_file.name, type=db_file.type, pinned_by=user.id)
#     father.session.add(new_pin)
#     father.session.commit()

#     tag = base.get_album_tags(album_id)
#     tags = list(set([i for i in tags if re.fullmatch(r'[a-zа-я\-\_\*\+\.]{1,16}', i, re.I)]))
#     for t in tags:
#         father.session.add(tag(file_album_id=new_pin.id, tag=t, added_by=user.id))
#     father.session.commit()


#     return schemes.files.File(id=db_file.id, name=db_file.name, created_at=db_file.created_at, created_by=db_file.created_by, type=db_file.type, public=public)