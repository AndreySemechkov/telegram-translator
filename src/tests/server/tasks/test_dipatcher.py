
from unittest.mock import patch
from dotenv import load_dotenv
import pytest
from src.server.tasks.scraper import fetch
from src.tests.test_base import TestBase
from src.server.tasks.dispatcher import handler

class TestDipatcher(TestBase):
    @pytest.mark.skip("This test is for local dev and shouldn't run without .env setup!")
    def test_handler_in_cloud(self):
        load_dotenv()
        handler("", None)
        
    @patch('boto3.client')
    @patch('src.server.tasks.dispatcher.get_channels')
    def test_handler(self, mocked_function, mock_boto3_client):
        mocked_function.return_value = [{"channelName":"kuku"},{"channelName": "blat"}]
        mock_eventbridge = mock_boto3_client('events')
        mock_eventbridge.put_events.return_value = {
            'FailedEntryCount': 0,  # Modify this value
            'Entries': [],  # Modify this list as needed
        }
        handler("", None)
        assert len(mock_eventbridge.put_events.call_args.kwargs['Entries']) == 2