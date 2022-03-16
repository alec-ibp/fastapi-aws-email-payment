from typing import Dict, List

from models import RoleType, ComplaintState
from models import complaint
from db.init_db import database
from schemas.request.complaint import ComplaintIn
from schemas.response.complaint import ComplaintOut

class ComplaintManager:
    @staticmethod
    async def get_all(user: Dict) -> List[ComplaintOut]:
        query = complaint.select()

        if user["role"] == RoleType.approver:
            query = query.where(complaint.c.status == ComplaintState.pendding)
        
        elif user["role"] == RoleType.complainer:
            query = query.where(complaint.c.complainer_id == user["id"])

        return await database.fetch_all(query)

    @staticmethod
    async def create(complaint_data: ComplaintIn, user: Dict):
        complaint_data["complainer_id"] = user["id"]
        _id = await database.execute(complaint.insert().values(complaint_data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == _id))
        
    @staticmethod
    async def delete(complaint_id: int):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))
        