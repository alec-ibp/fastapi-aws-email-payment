from fastapi import APIRouter, Depends, Request

from typing import List

from managers.auth import is_complainer, oauth2_schema
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
    dependencies=[Depends(oauth2_schema)],
)
async def delete_complaint(complaint_id: int):
    await ComplaintManager.delete(complaint_id)