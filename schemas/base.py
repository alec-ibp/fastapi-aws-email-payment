from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    email: EmailStr


class BaseComplaint(BaseModel):
    title: str
    description: str
    amount: float
