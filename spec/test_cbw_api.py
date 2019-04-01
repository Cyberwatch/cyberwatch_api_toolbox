"""Test file for cbw_api.py"""

from cbw_api_toolbox.cbw_api import CBWApi
from cbw_api_toolbox.cbw_objects.cbw_server import CBWServer

import vcr  # pylint: disable=import-error
import pytest  # pylint: disable=import-error

# To generate a new vcr cassette:
# - DO NOT CHANGE THE API_URL
# - Add your local credentials API_KEY and SECRET_KEY
# - Execute the test a first time, it should generate the cassette
# - Remove your credentials
# - relaunch the test. everything should work.


API_KEY = ''
SECRET_KEY = ''
API_URL = 'http://localhost'


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

    def test_servers(self): # pylint: disable=no-self-use
        """Tests for servers method"""
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/servers_ok.yaml'):
            response = CBWApi(API_URL, API_KEY, SECRET_KEY).servers()
            assert isinstance(response, list) is True
            for server in response:
                assert isinstance(server, CBWServer) is True

    def test_server(self): # pylint: disable=no-self-use
        """Tests for server method"""
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/server_ok.yaml'):
            response = CBWApi(
                API_URL,
                API_KEY,
                SECRET_KEY).server('25b4c2428fde60c311fb095e2083b33f')
            assert isinstance(response, CBWServer) is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/server_failed.yaml'):
            response = CBWApi(API_URL, API_KEY, SECRET_KEY).server('wrong_id')
            assert isinstance(response, CBWServer) is False

    def test_get_detailed_servers(self): # pylint: disable=no-self-use
        """Tests for get_detailed_servers method"""
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/get_detailed_servers.yaml'):
            response = CBWApi(API_URL, API_KEY, SECRET_KEY).get_detailed_servers()
            assert isinstance(response, list) is True
            for server in response:
                assert isinstance(server, CBWServer) is True
