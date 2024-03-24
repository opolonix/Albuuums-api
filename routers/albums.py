from fastapi import Depends, APIRouter
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from fastapi import Response, Request
import core.schemes as schemes
from core.father import Father
from models import base
from sqlalchemy import and_, or_
father = Father()

router = APIRouter(
    prefix="/albums",
    tags=["Альбомы"]
)

@router.post("/new")
async def new_album(album: Annotated[schemes.albums.New, Depends()], response: Response, request: Request) -> schemes.albums.fullAlbum:
    token = request.cookies.get("x-auth-key") if not request.headers.get("x-auth-key") else request.headers.get("x-auth-key")

    try: user: base.User = await father.verify(token=token, request=request, response=response)
    except HTTPException: raise HTTPException(status_code=403, detail="Not authorized")

    """
        id = Column(Integer, primary_key=True, autoincrement=True)
        private: bool = Column(BOOLEAN, default=True)
        created_at: datetime = Column(DateTime, default=datetime.now(pytz.timezone('Europe/Moscow')))
        created_by = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
        description = Column(String(512), default=None)
    """
    meta = base.albumsMeta(private=album.private, created_by=user.id, name=album.name, description=album.description)
    father.session.add(meta)
    father.session.commit()
    """
        id = Column(Integer, primary_key=True, autoincrement=True)
        album_id: int = Column(Integer)
        client_id: int = Column(Integer)
        editor: bool = Column(BOOLEAN, default=False)
        viewer: bool = Column(BOOLEAN, default=True)
        created_at = Column(DateTime, default=datetime.now(pytz.timezone('Europe/Moscow')))
        accessed_by = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    """

    access = base.albumsAccess(album_id=meta.id, client_id=user.id, editor=True, accessed_by=user.id)
    father.session.add(access)
    father.session.commit()

    base.get_album(meta.id)
    base.get_album_tags(meta.id)

    father.session.commit()

    return schemes.albums.fullAlbum(id=meta.id, album_cover_id=None, private=album.private, editor=True, name=meta.name, description=meta.description, files=[], tags=[])

@router.get("/get-my-albums")
async def getting_your_albums(response: Response, request: Request):

    token = request.cookies.get("x-auth-key") if not request.headers.get("x-auth-key") else request.headers.get("x-auth-key")

    try: user: base.User = await father.verify(token=token, request=request, response=response)
    except HTTPException: raise HTTPException(status_code=403, detail="Not authorized")

    album_metas: list[base.albumsMeta] = father.session.query(base.albumsMeta).filter(base.albumsMeta.created_by == user.id).all()
    albums_list = []


    for meta in album_metas:
        # avatar = father.session.query(base.get_album(meta.id)).first()
        avatar = father.session.query(base.get_album(meta.id)).first()
        print(avatar)
        tags = father.session.query(base.get_album_tags(meta.id)).all()
        tags = [schemes.albums.Tags(tag=t.tag, file_album_id=t.file_album_id) for t in tags]
        albums_list.append(schemes.albums.Album(id=meta.id, album_cover_id=avatar.file_id if avatar else None, name=meta.name, private=meta.private, editor=True, description=meta.description, tags=tags))
    return albums_list
    # return schemes.albums.Albums(albums=albums)

@router.get("/{album_id}")
async def getting_info(album_id: str, response: Response, request: Request) -> schemes.albums.fullAlbum:

    token = request.cookies.get("x-auth-key") if not request.headers.get("x-auth-key") else request.headers.get("x-auth-key")

    try: user: base.User = await father.verify(token=token, request=request, response=response)
    except HTTPException: raise HTTPException(status_code=403, detail="Not authorized")

    album_access: base.albumsAccess = father.session.query(base.albumsAccess).filter(base.albumsAccess.client_id == user.id, base.albumsAccess.album_id == album_id).first()

    if not album_access: raise HTTPException(status_code=403, detail="There is no access or the album does not exist")

    meta: base.albumsMeta = father.session.query(base.albumsMeta).filter(base.albumsMeta.id == album_access.album_id).first()

    tags = father.session.query(base.get_album_tags(meta.id)).all()
    files = father.session.query(base.get_album(meta.id)).all()
    tags = [schemes.albums.Tags(tag=t.tag, file_album_id=t.file_album_id) for t in tags]
    files = [schemes.albums.File(id=f.id, file_id=f.file_id, name=f.name, type=f.type, pinned_by=f.pinned_by, pinned_at=f.pinned_at, tags=tags) for f in files]

    return schemes.albums.fullAlbum(
        id=meta.id, 
        album_cover_id=files[0].file_id if len(files) != 0 else None, 
        private=meta.private, 
        editor=album_access.editor, 
        name=meta.name, 
        description=meta.description, 
        files=files,
        tags=tags
    )

@router.delete("/drop/{album_id}")
async def drop_album(album_id: str, response: Response, request: Request) -> schemes.albums.fullAlbum:

    token = request.cookies.get("x-auth-key") if not request.headers.get("x-auth-key") else request.headers.get("x-auth-key")

    try: user: base.User = await father.verify(token=token, request=request, response=response)
    except HTTPException: raise HTTPException(status_code=403, detail="Not authorized")

    album_access: base.albumsAccess = father.session.query(base.albumsAccess).filter(base.albumsAccess.client_id == user.id, base.albumsAccess.album_id == album_id).first()

    if not album_access: raise HTTPException(status_code=403, detail="There is no access or the album does not exist")

    meta: base.albumsMeta = father.session.query(base.albumsMeta).filter(base.albumsMeta.id == album_access.album_id).first()

    tags = father.session.query(base.get_album_tags(meta.id)).all()
    files = father.session.query(base.get_album(meta.id)).all()
    tags = [schemes.albums.Tags(tag=t.tag, file_album_id=t.file_album_id) for t in tags]
    files = [schemes.albums.File(id=f.id, file_id=f.file_id, name=f.name, type=f.type, pinned_by=f.pinned_by, pinned_at=f.pinned_at, tags=tags) for f in files]

    return schemes.albums.fullAlbum(
        id=meta.id, 
        album_cover_id=files[0].file_id if len(files) != 0 else None, 
        private=meta.private, 
        editor=album_access.editor, 
        name=meta.name, 
        description=meta.description, 
        files=files,
        tags=tags
    )