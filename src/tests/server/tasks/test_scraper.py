import asyncio
import json
from unittest.mock import Mock, patch
from dotenv import load_dotenv
import pytest
from src.server.tasks.scraper import fetch, scrape_feed
from src.server.tasks.scraper_utils import get_html_converter, get_message_data
from src.tests.test_base import TestBase
from src.server.database import DBMessage
from src.server.events import EventBridgeEvent

class TestScraper(TestBase):
  
    def test_when_given_msg_then_get_message_data_returns_data(self, mock_google_env_var):
        with open("src/tests/server/tasks/test_data/message.json", 'r', encoding='utf-8') as json_file:
            msg = json.load(json_file)

        mock_client = Mock()
        mock_client.translations().list.return_value.execute.return_value = {
            "translations": [{"translatedText": "Hello, world!"}]
        }
        data = asyncio.run(get_message_data(msg, "blat", get_html_converter(), mock_client))
        assert data is not None
        # Add more validators here
    
    #to run the scraper localy, set the dev key and mongo url
    @pytest.mark.skip("This test is for local dev and shouldn't run without setup the keys!")
    def test_handler(self):
        load_dotenv()
        fetch("", None)



    @pytest.mark.parametrize("translate,expected_data", [
        (
            {
                "translations": [{"translatedText": "Translated to Hebrew"}]
            },
        # Expected data 
        [
            DBMessage(
                msgId = 39838,
                msgOrig = "",
                msgEN = "Translated to English",
                msgHE = "Translated to Hebrew",
                username = "nasralla",
                mediaURL = "https://tg.i-c-a.su/media/nasralla/39838/preview",
                date = 1697185537),
        ]),
        (
        {"translations": [{"translatedText": "hofhim alehem tovim otam"}]},
        # Expected data 
        [
            DBMessage(
                msgId = 39838,
                msgOrig = "",
                msgEN = "Yet Another Translation",
                msgHE = "hofhim alehem tovim otam",
                username = "nasralla",
                mediaURL = "https://tg.i-c-a.su/media/nasralla/39838/preview",
                date = 1697185537)
        ],)
    ])
    def test_fetch_data(self, translate, expected_data, mock_google_env_var, mock_db_env_vars, mock_response, mock_event):

        actual = []
        # Mock the requests.get() method to return the mock JSON response
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_response
            with patch('src.server.database.MongoConn') as mock_mongo:    
                with patch('src.server.tasks.scraper_utils.persist_msg_data') as persist_mock:
                    with patch('src.server.tasks.scraper_utils.get_google_translate_service') as get_google_mock:
                        with patch('src.server.tasks.scraper_utils.translate') as translate_mock:
                            # Mock the API responses
                            translate_mock.return_value = translate
                            mock_instance = mock_mongo.return_value
                            mock_instance.doesExist.return_value = False
                            actual = asyncio.run(scrape_feed(EventBridgeEvent.parse_event(mock_event)))

        # validate actual is as expected
        assert len(actual) == 1, f"number of msgs we actually got{len(actual)} differs from expected"
        date = actual[0].date
        assert actual[0].date == expected_data[0].date, f"date {date} is wrong"
        assert actual[0].msgHE == expected_data[0].msgHE, f"msgHE {actual[0].msgHE} is wrong"
        # TODO: Additional assertions can be added based on our specific requirements and schema
