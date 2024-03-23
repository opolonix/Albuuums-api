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
from sqlalchemy import or_


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
            or_(base.File.created_by == user.id, base.File.public == True)
        ).first()
    else:
        db_file: base.File = father.session.query(base.File).filter(base.File.public == True).first()

    if db_file:
        file_path = f'files/{hex(db_file.id)}'
        filename = f'{db_file.name}.{db_file.type}'
        media_type = 'image/jpeg' if db_file.type == 'jpg' else 'image/png' if db_file.type == 'png' else 'video/mp4'
        return StreamingResponse(open(file_path, "rb"), media_type=media_type)
    else:
        raise HTTPException(400, "invalid file_id")




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

    """Прикрепление файла в альбом"""

    new_pin = base.get_album(album_id)(file_id=db_file.id, name=db_file.name, type=db_file.type, pinned_by=user.id)
    father.session.add(new_pin)
    father.session.commit()

    tag = base.get_album_tags(album_id)
    tags = list(set([i for i in tags if len(i) != 0 and len(i) <= 16]))
    for t in tags:
        father.session.add(tag(file_album_id=new_pin.id, tag=t, added_by=user.id))
    father.session.commit()

    if not os.path.exists(f'files/{hex(db_file.id)}'): open(f'files/{hex(db_file.id)}', "wb+").write(f)

    return schemes.files.File(id=db_file.id, name=db_file.name, created_at=db_file.created_at, created_by=db_file.created_by, type=db_file.type, public=public)

@router.delete("/drop/{id}")
async def drop_file(id):
    return HTTPException(status_code=200, detail="Successfully deleted")