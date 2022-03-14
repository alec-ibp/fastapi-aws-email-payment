
from fastapi import APIRouter, Depends, status

from managers.auth import oauth2_schema
from managers.user import UserManager
from schemas.request.user import UserLoginIn, UserRegisterIn


router = APIRouter(tags=["Authentication"])


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserRegisterIn) -> str:
    token: str = await UserManager.register(user_data.dict())
    return {"token": token}


@router.post(
    path="/login",
    status_code=200
)
async def login(user: UserLoginIn) -> str:
    token: str = await UserManager.login(user.dict())
    return {"token": token}
