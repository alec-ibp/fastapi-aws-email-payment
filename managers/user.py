from fastapi import HTTPException, status
from asyncpg import UniqueViolationError
from passlib.context import CryptContext

from typing import Dict, List

from managers.auth import AuthManager
from models import user, RoleType
from db.init_db import database
from schemas.response.user import UserOut

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    @staticmethod
    async def register(user_data: Dict) -> str:
        user_data["password"] = pwd_context.hash(user_data["password"])

        try:
            _id: int = await database.execute(user.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User email already exists!")

        user_db: Dict = await database.fetch_one(user.select().where(user.c.id == _id))
        return AuthManager.encode_token(user_db)

    @staticmethod
    async def login(user_data: Dict):
        user_db: Dict = await database.fetch_one(user.select().where(user.c.email == user_data["email"]))
        
        if not user_db:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect email or password")
        if not pwd_context.verify(user_data["password"], user_db["password"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect email or password")

        return AuthManager.encode_token(user_db)

    @staticmethod
    async def get_all_users() -> List[UserOut]:
        return await database.fetch_all(user.select())

    @staticmethod
    async def get_user_by_email(email: str) -> List[UserOut]:
        return await database.fetch_all(user.select().where((user.c.email == email)))
    
    @staticmethod
    async def change_roll(role: RoleType, user_id: int) -> None:
        _id = await database.fetch_one(user.select().where(user.c.id == user_id))
        
        if not _id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User doesn't exists!")
            
        await database.execute(user.update().where(user.c.id == user_id).values(role=role))
