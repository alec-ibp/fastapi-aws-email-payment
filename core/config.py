from pydantic import PostgresDsn
from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    SECRET_KEY: str
    AWS_ACCESS_KEY: str
    AWS_SECRECT_KEY: str
    AWS_S3_BUCKET_NAME: str
    AWS_REGION: str 

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = "UTF-8"


settings = Settings()
