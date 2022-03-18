import os
import uuid
from typing import Dict, List

from constants import TEMP_FILE_FOLDER
from db.init_db import database
from schemas.request.complaint import ComplaintIn
from schemas.response.complaint import ComplaintOut
from models import complaint, RoleType, ComplaintState
from services.s3 import s3Service
from services.ses import SESService
from utils.helpers import decode_photo

s3 = s3Service()
ses = SESService()

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
        encoded_photo = complaint_data.pop("encoded_photo")
        extension = complaint_data.pop("extension")
        name = f"{uuid.uuid4()}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, name)
        decode_photo(path, encoded_photo)
        complaint_data["photo_url"] = s3.upload(path, name, extension)
        os.remove(path)
        _id = await database.execute(complaint.insert().values(complaint_data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == _id))

    @staticmethod
    async def delete(complaint_id: int) -> None:
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))

    @staticmethod
    async def approve(_id):
        await database.execute(complaint.update().where(complaint.c.id == _id).values(status=ComplaintState.approved))
        ses.send_mail("Complaint approved", ["hzpulso@gmail.com"], "Congrats! your complaint was approved")

    @staticmethod
    async def reject(_id):
        await database.execute(complaint.update().where(complaint.c.id == _id).values(status=ComplaintState.rejected))
