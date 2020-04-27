"""Test file for cbw_api.py"""

from cbw_api_toolbox.cbw_api import CBWApi
from cbw_api_toolbox.cbw_objects.cbw_server import CBWCve
from cbw_api_toolbox.cbw_objects.cbw_group import CBWGroup
from cbw_api_toolbox.cbw_objects.cbw_host import CBWHost
from cbw_api_toolbox.cbw_objects.cbw_node import CBWNode
from cbw_api_toolbox.cbw_objects.cbw_security_issue import CBWSecurityIssue
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

    def test_servers(self):  # pylint: disable=no-self-use
        """Tests for servers method"""
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/servers_ok.yaml'):
            params = {
                'page': '1',
                'reboot_required' : 'false'
            }
            response = CBWApi(API_URL, API_KEY, SECRET_KEY).servers(params)
            assert isinstance(response, list) is True
            for server in response:
                assert isinstance(server, CBWServer) is True

    def test_server(self): # pylint: disable=no-self-use
        """Tests for server method"""
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/server_ok.yaml'):
            response = CBWApi(
                API_URL,
                API_KEY,
                SECRET_KEY).server("3")
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
            response = client.delete_server('6')
            assert response is True

    @staticmethod
    def test_update_server():
        """Tests for server method"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {
            "groups": [13, 12]
        }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_server.yaml'):
            response = client.update_server('6',
                                            info)
            assert response is True

        response = client.update_server('', info)
        assert response is False

        response = client.update_server(None, info)
        assert response is False

        info = {
            "groups": [None],
            "compliance_groups": [None]
        }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_server_with_group_none.yaml'):
            response = client.update_server('6', info)
            assert response is True

    @staticmethod
    def test_remote_accesses():
        """Tests for method remote_accesses"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/remote_accesses.yaml'):
            params = {
                'page': '1'
            }
            response = client.remote_accesses(params)
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
                "node_id": "1",  # precises the Cyberwatch source of the connection,
                "server_groups": "test, production",
                "priv_password": "",
                "auth_password": ""
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
            response = client.remote_access('15')
            assert isinstance(response, CBWRemoteAccess) is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/remote_access_wrong_id.yaml'):
            response = client.remote_access('wrong_id')
            assert isinstance(response, CBWRemoteAccess) is False

    @staticmethod
    def test_delete_remote_access():
        """Tests for method delete_remote_access"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_remote_access.yaml'):
            response = client.delete_remote_access('15')
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
            response = client.update_remote_access('15', info)

            assert isinstance(response, CBWRemoteAccess) is True

        info["address"] = "10.10.11.228"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_remote_access_id_none.yaml'):
            response = client.update_remote_access(None, info)

            assert isinstance(response, CBWRemoteAccess) is False

        info["type"] = ""

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_remote_access_without_type.yaml'):
            response = client.update_remote_access('15', info)

            assert response.type == "CbwRam::RemoteAccess::Ssh::WithPassword"


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
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/groups.yaml'):
            response = client.groups()
        for group in response:
            assert isinstance(group, CBWGroup) is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/group.yaml'):
            response = client.group('12')

            assert isinstance(response, CBWGroup) is True

        params = {
            "name": "test", #Required, name of the group
            "description": "test description", #Description of the created group
        }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/create_group.yaml'):
            response = client.create_group(params)

            assert isinstance(response, CBWGroup) is True

        params["name"] = "test_change"
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_group.yaml'):
            response = client.update_group('12', params)

            assert isinstance(response, CBWGroup) is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_group.yaml'):
            response = client.delete_group('12')

            assert isinstance(response, CBWGroup) is True

    @staticmethod
    def test_deploy():
        """Tests for method test_deploy_remote_access"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/test_deploy.yaml'):
            response = client.test_deploy_remote_access('15')

            assert isinstance(response, CBWRemoteAccess) is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/test_deploy_failed.yaml'):
            response = client.test_deploy_remote_access('wrong_id')

            assert isinstance(response, CBWRemoteAccess) is False

    @staticmethod
    def test_users():
        """Tests for method users"""

        params = {
            "auth_provider": "local_password"
        }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/users.yaml'):
            response = CBWApi(API_URL, API_KEY, SECRET_KEY).users(params)
            for user in response:
                assert isinstance(user, CBWUsers) is True

    @staticmethod
    def test_user():
        """Tests for method user"""
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/user.yaml'):
            response = CBWApi(API_URL, API_KEY, SECRET_KEY).user('1')

            assert isinstance(response, CBWUsers) is True

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

    @staticmethod
    def test_update_cve_announcement():
        """Tests for method update_cve_announcement()"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)
        cve_code = 'CVE-2019-16768'
        params = {
            "score_custom": "7",
            "access_complexity": "access_complexity_low",
            "access_vector": "access_vector_adjacent_network",
            "availability_impact": "availability_impact_none",
            "confidentiality_impact": "confidentiality_impact_low",
            "integrity_impact": "integrity_impact_low",
            "privilege_required": "privilege_required_none",
            "scope": "scope_changed",
            "user_interaction": "user_interaction_required"
        }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_cve_announcement.yaml'):
            response = client.update_cve_announcement(cve_code, params)
        assert isinstance(response, CBWCve) is True

    @staticmethod
    def test_delete_cve_announcement():
        """Tests for method delete_cve_announcement()"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)
        cve_code = 'CVE-2019-16768'
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_cve_announcement.yaml'):
            response = client.delete_cve_announcement(cve_code)
        assert isinstance(response, CBWCve) is True

    @staticmethod
    def test_nodes():
        """Tests for method nodes()"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)
        params = {
            'page': '1',
        }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/nodes.yaml'):
            response = client.nodes(params)
        for node in response:
            assert isinstance(node, CBWNode) is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/node.yaml'):
            response = client.node('1')

            assert isinstance(response, CBWNode) is True

        params = {
            "new_id": "1"
        }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_node.yaml'):
            response = client.delete_node('2', params)

            assert isinstance(response, CBWNode) is True

    @staticmethod
    def test_host():
        """Tests for method hosts"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/hosts.yaml'):
            response = client.hosts()
        for host in response:
            assert isinstance(host, CBWHost) is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/host.yaml'):
            response = client.host('12')

            assert isinstance(response, CBWHost) is True

        params = {
            "target": "192.168.1.2",
            "node_id": "1"
            }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/create_host.yaml'):
            response = client.create_host(params)

            assert isinstance(response, CBWHost) is True

        params["target"] = "192.168.2.3"
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_host.yaml'):
            response = client.update_host('12', params)

        assert isinstance(response, CBWHost) is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_host.yaml'):
            response = client.delete_host('12')

            assert isinstance(response, CBWHost) is True

    @staticmethod
    def test_update_server_cve():
        """Tests for server method"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {
            "comment": "test"
        }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_server_cve.yaml'):
            response = client.update_server_cve('9', "CVE-2019-3028", info)
            assert isinstance(response, CBWServer) is True

        info = {
            "ignored": "true"
        }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_server_cve_ignored.yaml'):
            response = client.update_server_cve('9', "CVE-2019-3028", info)
            assert isinstance(response, CBWServer) is True

    @staticmethod
    def test_security_issues():
        """Tests for method security_issues"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/security_issues.yaml'):
            params = {
                'page': '1'
            }
            response = client.security_issues(params)
            assert isinstance(response, list) is True
            for issue in response:
                assert isinstance(issue, CBWSecurityIssue) is True

    @staticmethod
    def test_create_security_issue():
        """Tests for method security_issue"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {
            "description": "Test",
            "level": "level_critical",
            "score": "5",
        }

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/create_security_issue.yaml'):
            response = client.create_security_issue(info)

            assert isinstance(response, CBWSecurityIssue) is True

    @staticmethod
    def test_update_security_issue():
        """Tests for update remote method"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {
            "description": "Test update",
            "level": "level_critical",
            "score": "5",
        }

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_security_issue.yaml'):
            response = client.update_security_issue('2', info)

            assert isinstance(response, CBWSecurityIssue) is True

        info["level"] = "level_test"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_security_issue_wrong_level.yaml'):
            response = client.update_security_issue("2", info)

            assert isinstance(response, CBWSecurityIssue) is False


    @staticmethod
    def test_delete_security_issue():
        """Tests for method delete_security_issue"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_security_issue.yaml'):
            response = client.delete_security_issue('1')
            assert isinstance(response, CBWSecurityIssue) is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_security_issue_wrong_id.yaml'):
            response = client.delete_security_issue('wrong_id')
            assert isinstance(response, CBWSecurityIssue) is False
