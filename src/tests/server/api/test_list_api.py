import json
from unittest.mock import patch
from src.server.api.get_list import get_list as list_api

MOCK_DB_DATA = {
    "documents": [
        {
            "msgId": 1,
            "msgOrig": "Sample message",
            "msgHE": "Sample message in Hebrew",
            "msgEN": "Sample message in English",
            "username": "sample_username",
            "date": 123456789,
        },
        {
            "msgId": 2,
            "msgOrig": "Another sample message",
            "msgHE": "Another sample message in Hebrew",
            "msgEN": "Another sample message in English",
            "username": "sample_username",
            "date": 123456789,
        },
    ],
    "totalDocuments": 2,
}


class TestListAPI:
    @patch("src.server.api.get_list.get_data")
    @patch("src.server.api.get_list.get_db_client")
    def test_list(self, mock_get_db_client, mock_get_data):
        mock_get_db_client.return_value = None
        mock_get_data.return_value = MOCK_DB_DATA

        event = {"queryStringParameters": {"limit": "10", "page": "1"}}
        response = list_api(event, None)

        assert response["statusCode"] == 200
        self.assert_headers(response)
        expected_messages = [
            {
                "id": 1,
                "title": "Sample message",
                "message": "Sample message",
                "username": "sample_username",
                "has_media": False,
                "media_url": "",
                "english": "Sample message in English",
                "hebrew": "Sample message in Hebrew",
                "date": 123456789,
                "link": "https://t.me/sample_username/1",
            },
            {
                "id": 2,
                "title": "Another sample message",
                "message": "Another sample message",
                "username": "sample_username",
                "has_media": False,
                "media_url": "",
                "english": "Another sample message in English",
                "hebrew": "Another sample message in Hebrew",
                "date": 123456789,
                "link": "https://t.me/sample_username/2",
            },
        ]
        assert response["body"] == self.response_schema(expected_messages, 2)

    @patch("src.server.api.get_list.get_data")
    @patch("src.server.api.get_list.get_db_client")
    def test_list_with_query_no_results(self, mock_get_db_client, mock_get_data):
        mock_get_db_client.return_value = None
        mock_get_data.return_value = {"documents": [], "totalDocuments": 0}

        event = {
            "queryStringParameters": {"limit": "10", "page": "1", "query": "Hello"}
        }
        response = list_api(event, None)

        assert response["statusCode"] == 200
        self.assert_headers(response)
        expected_messages = []
        assert response["body"] == self.response_schema(expected_messages, 0)

    @patch(
        "src.server.api.get_list.get_data",
        side_effect=Exception("Something went wrong"),
    )
    @patch("src.server.api.get_list.get_db_client")
    def test_list_with_exception(self, mock_get_db_client, mock_get_data):
        event = {
            "queryStringParameters": {
                "limit": "10",
                "page": "1",
                "query": "Another sample message",
            }
        }
        response = list_api(event, None)

        assert response["statusCode"] == 500
        assert response["body"] == json.dumps({"message": "Something went wrong"})

    # Test Helpers
    def assert_headers(self, response):
        assert response["headers"]["Access-Control-Allow-Origin"] == "*"
        assert response["headers"]["Access-Control-Allow-Headers"] == "Content-Type"
        assert (
            response["headers"]["Access-Control-Allow-Methods"]
            == "GET, POST, PUT, DELETE"
        )

    def response_schema(self, messages, messages_count):
        return json.dumps(
            {
                "messages": messages,
                "totalCount": messages_count,
            }
        )
