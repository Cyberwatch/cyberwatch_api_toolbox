"""Test file for cbw_api.py"""

from cbw_api_toolbox.cbw_api import CBWApi
from cbw_api_toolbox.cbw_objects.cbw_server import CBWCve
from cbw_api_toolbox.cbw_objects.cbw_group import CBWGroup
from cbw_api_toolbox.cbw_objects.cbw_server import CBWServer
from cbw_api_toolbox.cbw_objects.cbw_users import CBWUsers
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
API_URL = 'https://localhost'


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
                SECRET_KEY).server('3a239fd5dcaff8660ba7da1df1f3a247')
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
            response = client.delete_server('3a239fd5dcaff8660ba7da1df1f3a247')
            assert response is True

    @staticmethod
    def test_update_server():
        """Tests for server method"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {
            "groups": "production,Development",
            "compliance_groups": "Anssi"
        }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_server.yaml'):
            response = client.update_server('6b9648e93ae9207298be61de21e18a08',
                                            info)
            assert response is True

        response = client.update_server('', info)
        assert response is False

        response = client.update_server(None, info)
        assert response is False

        info = {
            "groups": None,
            "compliance_groups": None
        }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_server_with_group_none.yaml'):
            response = client.update_server('6b9648e93ae9207298be61de21e18a08', info)
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
                "node": "master",  # precises the Cyberwatch source of the connection,
                "server_groups": "test, production"
                }

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/create_remote_access.yaml'):
            response = client.create_remote_access(info)

            assert isinstance(response, CBWRemoteAccess) is True

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
            response = client.remote_access('7')
            assert isinstance(response, CBWRemoteAccess) is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/remote_access_wrong_id.yaml'):
            response = client.remote_access('wrong_id')
            assert isinstance(response, CBWRemoteAccess) is False

    @staticmethod
    def test_delete_remote_access():
        """Tests for method delete_remote_access"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_remote_access.yaml'):
            response = client.delete_remote_access('13')
            assert response is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_remote_access_wrong_id.yaml'):
            response = client.delete_remote_access('wrong_id')
            assert response is False

    @staticmethod
    def test_update_remote_access():
        """Tests for update remote method"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {"type": "CbwRam::RemoteAccess::Ssh::WithPassword",
                "address": "10.10.10.228",
                "port": "22",
                "login": "loginssh",
                "password": "passwordssh",
                "key": "",
                "node": "master"
                }

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_remote_access.yaml'):
            response = client.update_remote_access('7', info)

            assert response is True

        info["address"] = "10.10.11.228"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_remote_access_id_none.yaml'):
            response = client.update_remote_access(None, info)

            assert response is False

        info["type"] = ""

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_remote_access_without_type.yaml'):
            response = client.update_remote_access('14', info)

            assert response is False

    @staticmethod
    def test_cve_announcement():
        """Tests for method cve_announcement"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/cve_announcement.yaml'):
            response = client.cve_announcement('CVE-2017-0146')

            assert isinstance(response, CBWCve) is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/cve_announcement_failed.yaml'):
            response = client.cve_announcement('wrong_id')

            assert isinstance(response, CBWCve) is False

    @staticmethod
    def test_group():
        """Tests for method groups"""

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/groups.yaml'):
            response = CBWApi(API_URL, API_KEY, SECRET_KEY).groups()
            for group in response:
                assert isinstance(group, CBWGroup) is True

    @staticmethod
    def test_deploy():
        """Tests for method test_deploy_remote_access"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/test_deploy.yaml'):
            response = client.test_deploy_remote_access('14')

            assert isinstance(response, CBWRemoteAccess) is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/test_deploy_failed.yaml'):
            response = client.test_deploy_remote_access('wrong_id')

            assert isinstance(response, CBWRemoteAccess) is False

    @staticmethod
    def test_users():
        """Tests for method users"""

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/users.yaml'):
            response = CBWApi(API_URL, API_KEY, SECRET_KEY).users()
            for user in response:
                assert isinstance(user, CBWUsers) is True

    @staticmethod
    def test_cve_announcements():
        """Tests for method cve_announcements()"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)
        params = {
            'page': '1'
        }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/cve_announcements.yaml'):
            response = client.cve_announcements(params)
        for cve in response:
            assert isinstance(cve, CBWCve) is True
