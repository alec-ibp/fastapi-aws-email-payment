from pydantic import BaseModel


class BaseComplaint(BaseModel):
    title: str
    description: str
    photo_url: str
    amount: float
    