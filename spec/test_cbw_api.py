"""Test file for cbw_api.py"""

from cbw_api_toolbox.cbw_api import CBWApi
import vcr  # pylint: disable=import-error
import pytest  # pylint: disable=import-error

API_KEY = 'b2mVyRFut9LnK5yAn0uwqe7JklLIUOkn9lgqx3GMTOw='
SECRET_KEY = 'QqSfOLlbkhrrhmnNfJW0mkCx4daURHysF4hk8ydRUoa1Kw7gvwhNuGzSrso5JNiSs/ldb0eez4JowCIXCVlcsA=='  # pylint: disable=line-too-long
API_URL = 'http://10.10.1.129'


class TestCBWApi:
    """Test for class CBWApi"""

    def test_ping(self):  # pylint: disable=no-self-use
        """Tests for method ping"""
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/ping_ok.yaml'):
            response = CBWApi(API_URL, API_KEY, SECRET_KEY).ping()
            assert response is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/ping_without_secret_key.yaml'):
            response = CBWApi(API_URL, API_KEY, '').ping()
            assert response is False

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/ping_without_api_key.yaml'):
            response = CBWApi(API_URL, '', SECRET_KEY).ping()
            assert response is False

        with pytest.raises(SystemExit) as exc:
            CBWApi('', API_KEY, SECRET_KEY).ping()
        assert exc.value.code == -1
