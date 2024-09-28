import pytest
from src.server.database import DBCredentials
from src.tests.test_base import TestBase
from src.server.api.language import Language
from src.server.database import DBMessage


class TestDBUtils(TestBase):
    def test_when_missing_env_vars_then_dbcreds_fails(self):
        self.del_db_env_vars()
        with pytest.raises(Exception):
            DBCredentials.from_env()

    def test_when_env_vars_then_dbcreds(self, mock_db_env_vars):
        assert DBCredentials.from_env() is not None

    def test_message(self) -> None:
        assert (
            DBMessage(
                msgId=123,
                msgOrig="Original",
                msgHE="Hebrew",
                msgEN="English",
                username="User",
                mediaURL="Media URL",
                date=1234,
            )
            is not None
        )
