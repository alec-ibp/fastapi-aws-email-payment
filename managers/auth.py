import jwt
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from typing import Dict, Optional
from datetime import datetime, timedelta

from models import user
from core.config import settings
from db.init_db import database


class AuthManager:
    @staticmethod
    def encode_token(user: Dict) -> Optional[str]:
        try:
            payload: Dict = {
                "sub": user["id"],
                "exp": datetime.utcnow() + timedelta(minutes=120)
            }

            return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        except Exception as ex:
            raise ex


class CustomHttpBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:

        result = await super().__call__(request)

        try:
            payload = jwt.decode(result.credentials, settings.SECRET_KEY, algorithms=["SH256"])

            user_data = await database.fetch_one(user.select().where(user.c.id == payload["sub"]))
            request.state.user = user_data
            return user_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
 
 
oauth2_schema = CustomHttpBearer()