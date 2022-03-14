from pydantic import PostgresDsn
from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    SECRET_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = "UTF-8"

settings = Settings()
