import boto3
from pydantic import EmailStr
from core.config import settings


class SESService:
    def __init__(self) -> None:
        self.key = settings.AWS_ACCESS_KEY
        self.secret = settings.AWS_SECRECT_KEY
        self.region = settings.AWS_REGION
        self.ses = boto3.client("ses", region_name=self.region, aws_access_key_id=self.key,
                                aws_secret_access_key=self.secret)

    def send_mail(self, subject: EmailStr, to_addresses: EmailStr, text_data: str):
        body = {
            "Text": {
                "Data": text_data,
                "Charset": "UTF-8"
            }
        }

        self.ses.send_email(Source="alejo1ibarra@gmail.com",
                            Destination={
                                "ToAddresses": to_addresses,
                                "CcAddresses": [],
                                "BccAddresses": [],
                            },
                            Message={
                                "Subject": {
                                    "Data": subject,
                                    "Charset": "UTF-8"
                                },
                                "Body": body
                                }
                            )
