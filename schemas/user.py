
from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    email: EmailStr


class UserRegisterIn(BaseUser):
    password: str
    firstname: str
    lastname: str
    iban: str


class UserLoginIn(BaseUser):
    password: str