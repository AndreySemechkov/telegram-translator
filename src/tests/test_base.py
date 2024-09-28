import os
import pytest
import json

class TestBase:
    
    @pytest.fixture
    def mock_db_env_vars(self):
        # Set the environment variable for the test
        os.environ["MONGO_DB_URL"] = "KUKU"

        # The fixture will yield the value you want to use for testing
        yield

        # Clean up: Unset the environment variable after the test
        del os.environ["MONGO_DB_URL"]
    
    @pytest.fixture
    def mock_response(self):
        # mocks messages feed from telegram
        with open(os.path.join(os.getcwd(), 'src/tests/data', 'messages.json'), 'r') as file:
            return json.load(file)
    
    @pytest.fixture
    def mock_event(self):
        # mocks messages feed from telegram
        with open(os.path.join(os.getcwd(), 'src/tests/data', 'dispatch_event.json'), 'r') as file:
            return json.load(file)
    
    def init_db_env_vars(self, url):
        os.environ["MONGO_DB_URL"] = url
    
    def del_db_env_vars(self):
        os.environ.pop("MONGO_DB_URL", None)

    @pytest.fixture   
    def mock_google_env_var(self):
        # Set the environment variable for the test
        os.environ["GOOGLE_TRANSLATE_API"] = "mocked_value"

        # The fixture will yield the value you want to use for testing
        yield

        # Clean up: Unset the environment variable after the test
        del os.environ["GOOGLE_TRANSLATE_API"]
        
    def init_google_env_vars(self, key):
        os.environ["GOOGLE_TRANSLATE_API"] = key
    
    def del_google_env_vars(self):
        os.environ.pop("GOOGLE_TRANSLATE_API", None)

