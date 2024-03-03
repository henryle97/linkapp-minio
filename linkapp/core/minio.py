import os
import random
from datetime import datetime, timedelta

from minio import Minio

MININO_ENDPOINT = os.getenv("MINI_ENDPOINT")
MININO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
MININO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")
MININO_BUCKET_NAME = os.getenv("MININO_BUCKET_NAME")

print(
    f"MININO_ENDPOINT: {MININO_ENDPOINT}"
    f"MININO_ACCESS_KEY: {MININO_ACCESS_KEY}"
    f"MININO_SECRET_KEY: {MININO_SECRET_KEY}"
    f"MININO_BUCKET_NAME: {MININO_BUCKET_NAME}"
)


class MinioHandler:
    __instance = None

    @staticmethod
    def get_instance():
        """Static access method."""
        if not MinioHandler.__instance:
            MinioHandler.__instance = MinioHandler(
                minio_url=MININO_ENDPOINT,
                access_key=MININO_ACCESS_KEY,
                secret_key=MININO_SECRET_KEY,
                bucket_name=MININO_BUCKET_NAME,
            )
        return MinioHandler.__instance

    def __init__(
        self,
        minio_url,
        access_key,
        secret_key,
        bucket_name,
    ):
        self.minio_url = minio_url
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.client = Minio(
            self.minio_url,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=False,
        )
        self.make_bucket()

    def make_bucket(self) -> str:
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
        return self.bucket_name

    def presigned_get_object(self, bucket_name, object_name):
        # Request URL expired after 7 days
        url = self.client.presigned_get_object(
            bucket_name=bucket_name,
            object_name=object_name,
            expires=timedelta(days=7),
        )
        return url

    def check_file_name_exists(self, bucket_name, file_name):
        try:
            self.client.stat_object(bucket_name=bucket_name, object_name=file_name)
            return True
        except Exception as e:
            print(f"[x] Exception: {e}")
            return False

    def put_object(self, file_data, file_name, content_type):
        try:
            datetime_prefix = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            object_name = f"{datetime_prefix}___{file_name}"
            while self.check_file_name_exists(
                bucket_name=self.bucket_name, file_name=object_name
            ):
                random_prefix = random.randint(1, 1000)
                object_name = f"{datetime_prefix}___{random_prefix}___{file_name}"

            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=file_data,
                content_type=content_type,
                length=-1,
                part_size=10 * 1024 * 1024,
            )
            url = self.presigned_get_object(
                bucket_name=self.bucket_name, object_name=object_name
            )
            data_file = {
                "bucket_name": self.bucket_name,
                "file_name": object_name,
                "url": url,
            }
            return data_file
        except Exception as e:
            raise Exception(e)
