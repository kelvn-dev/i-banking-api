import uuid

import boto3
from botocore.config import Config
from fastapi import HTTPException

from config.setting import settings
from enums.s3_enum import ContentDisposition
from utils.helper_utils import generate_random_string


class S3Service:
    def __init__(self):
        self.bucket_name = settings.aws_bucket
        self.presigned_url_expiry = 300  # hardcode 300s for this project
        self.client = boto3.client(
            service_name="s3",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            config=Config(signature_version="s3v4"),
        )

    def generate_presigned_get_url(
        self, key: str, content_disposition: ContentDisposition
    ):
        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            ExpiresIn=self.presigned_url_expiry,
            Params={
                "Bucket": self.bucket_name,
                "Key": key,
                "ResponseContentDisposition": content_disposition.value,
            },
        )

    def generate_presigned_post(
        self,
        file_extension: str,
        content_type: str,
    ):
        acl = "public-read"  # public all images for this project
        fields = {
            "acl": acl,
            "Content-Type": content_type,
        }
        key = f"{generate_random_string()}.{file_extension}"

        response = self.client.generate_presigned_post(
            Bucket=self.bucket_name,
            Key=key,
            ExpiresIn=self.presigned_url_expiry,
            Fields=fields,
            Conditions=[
                {"acl": acl},
                ["starts-with", "$Content-Type", f"{content_type.split('/')[0]}/"],
            ],
        )
        return response

    def delete_object(self, key):
        self.client.delete_object(Bucket=self.bucket_name, Key=key)


s3_service = S3Service()
