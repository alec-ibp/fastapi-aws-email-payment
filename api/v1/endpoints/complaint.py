from fastapi import APIRouter, Depends, Request, status

from typing import List

from managers.auth import is_admin, is_approver, is_complainer, oauth2_schema
from managers.complaint import ComplaintManager
from schemas.request.complaint import ComplaintIn
from schemas.response.complaint import ComplaintOut



router = APIRouter(tags=["Complaints"])


@router.get(
    path="/complaints",
    dependencies=[Depends(oauth2_schema)],
    response_model=List[ComplaintOut]
)
async def get_complaints(request: Request):
    user = request.state.user
    return await ComplaintManager.get_all(user)


@router.post(
    path="/complaints",
    dependencies=[Depends(oauth2_schema), Depends(is_complainer)],
    response_model=ComplaintOut
)
async def create_complaint(request: Request, complaint: ComplaintIn):
    user = request.state.user
    return await ComplaintManager.create(complaint.dict(), user)
    

@router.delete(
    path="/complaints/{complaint_id}",
    dependencies=[Depends(oauth2_schema), Depends(is_admin)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_complaint(complaint_id: int):
    await ComplaintManager.delete(complaint_id)


@router.put(
    path="/complaints/{complaint_id}/approve",
    dependencies=[Depends(oauth2_schema), Depends(is_approver)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def approve_complaint(complaint_id: int):
    await ComplaintManager.approve(complaint_id)


@router.put(
    path="/complaints/{complaint_id}/reject",
    dependencies=[Depends(oauth2_schema), Depends(is_approver)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def reject_complaint(complaint_id: int):
    await ComplaintManager.reject(complaint_id)