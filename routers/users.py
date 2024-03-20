from fastapi import Depends, APIRouter, Request, HTTPException

import schemes

from father import Father
father = Father()

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)

@router.get("/get-me")
async def get_yourself(request: Request):
    if not (token := request.cookies.get("x-auth-key")): # выкидывает если пользователя не существует
        pass
    user_id = await father.is_authorized(token)
    if not user_id: 
        return HTTPException(status_code=403, detail="Unauthorized")
    
    print(user_id)
# schemes.users.User(key="228", name="228")
    return [str(user_id)]

@router.get("/get/{username}")
async def get_user(username, request: Request) -> schemes.users.User:
    return schemes.users.User(key="228", name="228")

