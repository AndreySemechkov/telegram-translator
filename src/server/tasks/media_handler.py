import os
import requests
import boto3
from loguru import logger
from datetime import datetime


MEDIA_BUCKET_NAME = os.environ.get("MEDIA_BUCKET_NAME")
S3_CLIENT = boto3.client("s3")


class MediaType:
    IMAGE = "jpeg"
    VIDEO = "mp4"


class MediaHandler:
    def __init__(self, message: dict, channel: str):
        self.message = message
        self.msg_id = message.get("id")
        self.channel = channel

        self.set_media_properties(message.get("media"))

    def store(self) -> str:
        try:
            if not self.media or not self.msg_id:
                logger.info(f"No media or msg_id. Meesage is {self.message}")
                return None

            source_media_url = self.get_media_url_source()
            response: requests.Response = self.request_media_url(source_media_url)
            if not response:
                return None

            object_key = self.get_object_key()
            self.upload_file(object_key, response.content)

            logger.info(f"Succesfully uploaded {object_key}")
            return f"https://{MEDIA_BUCKET_NAME}.s3.amazonaws.com/{object_key}"

        except Exception as e:
            logger.error(f"MediaStore.store error: {str(e)}")
            return None

    def request_media_url(self, source_media_url: str) -> requests.Response:
        response = requests.get(source_media_url)
        if response.status_code != 200:
            logger.error(f"Failed to download media from {source_media_url}")
            return None

        return response

    def get_media_url_source(self):
        return f"https://tg.i-c-a.su/media/{self.channel}/{self.msg_id}"

    def get_formatted_date(self):
        current_date = datetime.now()
        return current_date.strftime("%Y/%m/%d")

    def get_object_key(self):
        return (
            f"{self.get_formatted_date()}/{self.channel}/{self.msg_id}/{self.media_id}.{self.media_type}"
        )

    def set_media_properties(self, media: dict):
        self.media = None
        if not media:
            return

        if media.get("_") == "messageMediaPhoto":
            self.media_type = MediaType.IMAGE
            self.media_id = media.get("photo").get("id")
            self.media = media
            return

        if media.get("_") == "messageMediaDocument":
            self.media_type = MediaType.VIDEO
            self.media_id = media.get("document").get("id")
            self.media = media
            return

    def upload_file(self, object_key: str, file_obj: bytes):
        S3_CLIENT.put_object(Bucket=MEDIA_BUCKET_NAME, Key=object_key, Body=file_obj)
