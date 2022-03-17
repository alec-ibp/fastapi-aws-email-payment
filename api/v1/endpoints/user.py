from fastapi import APIRouter, Depends, status

from typing import Optional, List

from managers.auth import is_admin, oauth2_schema
from managers.user import UserManager
from models.enums import RoleType
from schemas.response.user import UserOut

router = APIRouter(tags=["Users"])


@router.get(
    path="/users",
    dependencies=[Depends(oauth2_schema), Depends(is_admin)],
    response_model=List[UserOut]
)
async def get_users(email: Optional[str] = None):
    if email:
        return await UserManager.get_user_by_email(email)
    return await UserManager.get_all_users()

@router.put(
    path="/users/{user_id}/make_admin",
    dependencies=[Depends(oauth2_schema), Depends(is_admin)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def make_admin(user_id: int):
    await UserManager.change_roll(RoleType.admin, user_id)


@router.put(
    path="/users/{user_id}/make-approver",
    dependencies=[Depends(oauth2_schema), Depends(is_admin)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def make_approver(user_id: int):
    await UserManager.change_roll(RoleType.approver, user_id)