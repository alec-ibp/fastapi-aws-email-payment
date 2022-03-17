from models import RoleType
from schemas.base import BaseUser


class UserOut(BaseUser):
    id: int
    firstname: str
    lastname: str
    phone: str
    iban: str
    role: RoleType
    