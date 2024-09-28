import pytest
from unittest.mock import patch, MagicMock
from src.server.tasks.media_handler import MediaHandler, MediaType
from src.tests.test_base import TestBase

MOCK_BUCKET_NAME = "MOCK_BUCKET_NAME"
MOCK_CONTENT = b"MOCK_CONTENT"
MESSAGE_ID = 111
MEDIA_PHOTO_ID = 123
MEDIA_VIDEO_ID = 321
CHANNEL_NAME = "test_channel"
SOURCE_MEDIA_URL = f"https://tg.i-c-a.su/media/{CHANNEL_NAME}/{MESSAGE_ID}"
MOCK_FORMATTED_DATE = "2021/01/01"


class TestMediaHandler(TestBase):
    @pytest.fixture(scope="function")
    def mock_photo_media(self):
        return {
            "id": MESSAGE_ID,
            "media": {"_": "messageMediaPhoto", "photo": {"id": MEDIA_PHOTO_ID}},
        }

    @pytest.fixture(scope="function")
    def mock_video_media(self):
        return {
            "id": MESSAGE_ID,
            "media": {"_": "messageMediaDocument", "document": {"id": MEDIA_VIDEO_ID}},
        }

    @pytest.fixture(scope="function")
    def mock_without_media(self):
        return {"id": MESSAGE_ID}

    @pytest.fixture(scope="function")
    def mock_channel(self):
        return "test_channel"

    @pytest.fixture(scope="function")
    def media_handler_photo(self, mock_photo_media, mock_channel):
        return MediaHandler(mock_photo_media, mock_channel)

    @pytest.fixture(scope="function")
    def media_handler_video(self, mock_video_media, mock_channel):
        return MediaHandler(mock_video_media, mock_channel)

    @pytest.fixture(scope="function")
    def media_handler_no_media(self, mock_without_media, mock_channel):
        return MediaHandler(mock_without_media, mock_channel)

    @patch("src.server.tasks.media_handler.MEDIA_BUCKET_NAME", MOCK_BUCKET_NAME)
    @patch("src.server.tasks.media_handler.requests")
    def test_store_success_photo(self, mock_requests, media_handler_photo):
        mock_requests.get.return_value = self.get_200_mock_response()

        media_handler_photo.upload_file = MagicMock()
        media_handler_photo.get_formatted_date = MagicMock()
        media_handler_photo.get_formatted_date.return_value = MOCK_FORMATTED_DATE

        result = media_handler_photo.store()
        expected_object_key = f"{MOCK_FORMATTED_DATE}/{CHANNEL_NAME}/{MESSAGE_ID}/{MEDIA_PHOTO_ID}.{MediaType.IMAGE}"

        self.assert_sucess_store(
            expected_object_key, mock_requests, media_handler_photo, result
        )

    @patch("src.server.tasks.media_handler.MEDIA_BUCKET_NAME", MOCK_BUCKET_NAME)
    @patch("src.server.tasks.media_handler.requests")
    def test_store_success_video(self, mock_requests, media_handler_video):
        mock_requests.get.return_value = self.get_200_mock_response()

        media_handler_video.upload_file = MagicMock()
        media_handler_video.get_formatted_date = MagicMock()
        media_handler_video.get_formatted_date.return_value = MOCK_FORMATTED_DATE

        result = media_handler_video.store()
        expected_object_key = f"{MOCK_FORMATTED_DATE}/{CHANNEL_NAME}/{MESSAGE_ID}/{MEDIA_VIDEO_ID}.{MediaType.VIDEO}"

        self.assert_sucess_store(
            expected_object_key, mock_requests, media_handler_video, result
        )

    @patch("src.server.tasks.media_handler.MEDIA_BUCKET_NAME", MOCK_BUCKET_NAME)
    def test_store_no_media(self, media_handler_no_media):
        result = media_handler_no_media.store()
        assert result is None

    @patch("src.server.tasks.media_handler.requests")
    def test_store_request_failure(self, mock_requests, media_handler_photo):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests.get.return_value = mock_response

        media_handler_photo.upload_file = MagicMock()

        result = media_handler_photo.store()

        assert result is None
        mock_requests.get.assert_called_once_with(SOURCE_MEDIA_URL)
        media_handler_photo.upload_file.assert_not_called()

    def test_get_media_url_source(self, media_handler_photo):
        result = media_handler_photo.get_media_url_source()
        assert result == SOURCE_MEDIA_URL

    def test_set_media_properties_photo(self, media_handler_photo):
        media = {"_": "messageMediaPhoto", "photo": {"id": 456}}
        media_handler_photo.set_media_properties(media)
        assert media_handler_photo.media_type == MediaType.IMAGE
        assert media_handler_photo.media_id == 456
        assert media_handler_photo.media == media

    def test_set_media_properties_document(self, media_handler_photo):
        media = {"_": "messageMediaDocument", "document": {"id": 789}}
        media_handler_photo.set_media_properties(media)
        assert media_handler_photo.media_type == MediaType.VIDEO
        assert media_handler_photo.media_id == 789
        assert media_handler_photo.media == media

    def test_set_media_properties_no_media(self, media_handler_photo):
        media_handler_photo.set_media_properties(None)
        assert media_handler_photo.media is None

    @patch("src.server.tasks.media_handler.MEDIA_BUCKET_NAME", MOCK_BUCKET_NAME)
    @patch("src.server.tasks.media_handler.S3_CLIENT")
    def test_upload_file(self, mock_s3_client, media_handler_photo):
        media_handler_photo.upload_file("test_key", MOCK_CONTENT)
        mock_s3_client.put_object.assert_called_once_with(
            Bucket=MOCK_BUCKET_NAME, Key="test_key", Body=MOCK_CONTENT
        )

    # Test Helpers
    def get_200_mock_response(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = MOCK_CONTENT
        return mock_response

    # Assert Helpers
    def assert_sucess_store(
        self, expected_object_key, mock_requests, media_handler, result_url
    ):
        mock_requests.get.assert_called_once_with(SOURCE_MEDIA_URL)
        media_handler.upload_file.assert_called_once_with(
            f"{expected_object_key}", MOCK_CONTENT
        )
        assert (
            result_url
            == f"https://{MOCK_BUCKET_NAME}.s3.amazonaws.com/{expected_object_key}"
        )
