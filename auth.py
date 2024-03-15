from typing import Annotated, Optional
from fastapi import Depends, APIRouter
from pydantic import BaseModel

from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters

import schemes
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi import HTTPException
from uuid import UUID
from fastapi_sessions.backends.implementations import InMemoryBackend

from uuid import uuid4
from fastapi import FastAPI, Response

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"]
)

cookie_params = CookieParameters()

cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)


backend = InMemoryBackend[UUID, schemes.user.Session]()

class BasicVerifier(SessionVerifier[UUID, schemes.user.Session]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, schemes.user.Session],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: schemes.user.Session) -> bool:
        """If the session exists, it is valid"""
        return True
    
verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)
@router.post("/signin/LoginPassword")
async def users(user: Annotated[schemes.signin.LoginPassword, Depends()], response: Response) -> schemes.User:
    
    session = uuid4()
    data = schemes.user.Session(username="228")
    await backend.create(session, data)

    cookie.attach_to_response(response, session)

    return schemes.User(key="228", name="228")

@router.post("/signup/LoginPassword")
async def users(user: Annotated[schemes.signup.LoginPassword, Depends()], response: Response) -> schemes.User:
    
    session = uuid4()
    data = schemes.user.Session(username="228")
    await backend.create(session, data)

    cookie.attach_to_response(response, session)

    return schemes.User(key="228", name="228")
