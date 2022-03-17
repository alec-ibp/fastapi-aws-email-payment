from schemas.base import BaseUser


class UserRegisterIn(BaseUser):
    password: str
    firstname: str
    lastname: str
    phone: str
    iban: str


class UserLoginIn(BaseUser):
    password: str
