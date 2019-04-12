"""Test file for cbw_api.py"""

from cbw_api_toolbox.cbw_api import CBWApi
from cbw_api_toolbox.cbw_objects.cbw_server import CBWServer
from cbw_api_toolbox.cbw_objects.cbw_remote_access import CBWRemoteAccess

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

    @staticmethod
    def test_delete_server():
        """Tests for method delete_server"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        response = client.delete_server(None)
        assert response is False

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_server_without_server_id.yaml'):
            response = client.delete_server('wrong id')
            assert response is False

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_server_with_server_id.yaml'):
            response = client.delete_server('fd302ddb48d8634e948afdb84abd1db1')
            assert response is True

    @staticmethod
    def test_update_server():
        """Tests for server method"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_server.yaml'):
            response = client.update_server('7472cc6f37a6b5482193ca5184a88d44',
                                            "production,Development")
            assert response is True

        response = client.update_server('', "production,Development")
        assert response is False

        response = client.update_server(None, "Production,Development")
        assert response is False

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_server_with_group_none.yaml'):
            response = client.update_server('7472cc6f37a6b5482193ca5184a88d44', None)
            assert response is True

    @staticmethod
    def test_remote_accesses():
        """Tests for method remote_accesses"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/remote_accesses.yaml'):
            response = client.remote_accesses()
            assert isinstance(response, list) is True
            for remote in response:
                assert isinstance(remote, CBWRemoteAccess) is True

    @staticmethod
    def test_create_remote_access():
        """Tests for method remote_access"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {"type": "CbwRam::RemoteAccess::Ssh::WithPassword",
                "address": "X.X.X.X",
                "port": "22",
                "login": "loginssh",
                "password": "passwordssh",
                "key": "",  # precises the key of the connection
                "node": "master"  # precises the Cyberwatch source of the connection,
                }

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/create_remote_access.yaml'):
            response = client.create_remote_access(info)

            assert response is True

        info["address"] = ""

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/create_remote_access_failed_'
                              'without_address.yaml'):
            response = client.create_remote_access(info)

            assert response is False

    @staticmethod
    def test_remote_access():
        """Tests for method remote_access"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/remote_access.yaml'):
            response = client.remote_access('4')
            assert isinstance(response, CBWRemoteAccess) is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/remote_access_wrong_id.yaml'):
            response = client.remote_access('wrong_id')
            assert isinstance(response, CBWRemoteAccess) is False

    @staticmethod
    def test_delete_remote_access():
        """Tests for method delete_remote_access"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_remote_access.yaml'):
            response = client.delete_remote_access('6')
            assert response is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_remote_access_wrong_id.yaml'):
            response = client.delete_remote_access('wrong_id')
            assert response is False
