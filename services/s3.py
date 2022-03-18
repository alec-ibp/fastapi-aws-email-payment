import boto3
from fastapi import HTTPException, status

from core.config import settings


class s3Service:
    def __init__(self) -> None:
        self.key = settings.AWS_ACCESS_KEY
        self.secret = settings.AWS_SECRECT_KEY
        self.s3 = boto3.client("s3", aws_access_key_id=self.key, 
                                aws_secret_access_key=self.secret)

        self.bucket = settings.AWS_S3_BUCKET_NAME

    def upload(self, path: str, key: str, ext: str) -> str:
        try:
            self.s3.upload_file(
                path,
                self.bucket, 
                key,
                ExtraArgs={"ACL": "public-read", "ContentType": f"image/{ext}"}
            )
            return f"https://{self.bucket}.s3.amazonaws.com/{key}"
        except Exception as ex:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="S3 not available")
            