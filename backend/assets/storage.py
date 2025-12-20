import boto3
from django.conf import settings
from uuid import uuid4

class S3Storage:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION,
        )
        self.bucket = settings.S3_BUCKET_NAME

    def upload(self, user_id, file_obj, filename):
        ext = filename.split(".")[-1]
        key = f"users/{user_id}/assets/{uuid4()}.{ext}"

        self.client.upload_fileobj(
            file_obj,
            self.bucket,
            key,
            ExtraArgs={"ContentType": file_obj.content_type},
        )
        return key

    def delete(self, key):
        self.client.delete_object(Bucket=self.bucket, Key=key)

    def download(self, key: str) -> bytes:
        obj = self.client.get_object(
            Bucket=self.bucket,
            Key=key,
        )
        return obj["Body"].read()
