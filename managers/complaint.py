import os
import uuid
from typing import Dict, List

from db.init_db import database
from schemas.request.complaint import ComplaintIn
from schemas.response.complaint import ComplaintOut
from models import complaint, transaction, RoleType, ComplaintState
from services.s3 import s3Service
from services.ses import SESService
from services.wise import WiseService
from utils.helpers import decode_photo
from constants import TEMP_FILE_FOLDER

s3 = s3Service()
ses = SESService()
wise = WiseService()


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

        # use a transaction connection exm if the query for save complaint works but issue_transaction fails would be a problem so with database transaction we assure that all works
        async with database.transaction() as tconn:
            _id = await tconn._connection.execute(complaint.insert().values(complaint_data))
            await ComplaintManager.issue_transation(tconn, complaint_data["amount"], f"{user['firstname']} {user['lastname']}", user['iban'], _id)

        return await database.fetch_one(complaint.select().where(complaint.c.id == _id))

    @staticmethod
    async def delete(complaint_id: int) -> None:
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))

    @staticmethod
    async def approve(_id):
        await database.execute(complaint.update().where(complaint.c.id == _id).values(status=ComplaintState.approved))
        
        transaction_data = await database.fetch_one(transaction.select().where(transaction.c.complaint_id == _id))
        wise.fund_transfer(transaction_data["transfer_id"])

        ses.send_mail("Complaint approved", [
                      "hzpulso@gmail.com"], "Congrats! your complaint was approved")

    @staticmethod
    async def reject(_id):
        transaction_data = await database.fetch_one(transaction.select().where(transaction.c.complaint_id == _id))

        wise.cancel_funds(transaction_data["transfer_id"])
        await database.execute(complaint.update().where(complaint.c.id == _id).values(status=ComplaintState.rejected))

    @staticmethod
    async def issue_transation(tconn, amount, fullname, iban, complaint_id):

        quote_id = wise.create_quote(amount)
        recipient_id = wise.create_recipient_account(fullname, iban)
        transfer_id = wise.create_transfer(recipient_id, quote_id)

        data = {

            "quote_id": quote_id,
            "transfer_id": transfer_id,
            "target_account_id": str(recipient_id),
            "amount": amount,
            "complaint_id": complaint_id
        }    
        await tconn._connection.execute(transaction.insert().values(data))
