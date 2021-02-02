"""Test file for cbw_api.py"""

import vcr  # pylint: disable=import-error
import pytest  # pylint: disable=import-error
from cbw_api_toolbox.cbw_api import CBWApi

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

    @staticmethod
    def test_servers():
        """Tests for servers method"""

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/servers_ok.yaml'):

            validate_server = """cbw_object(id=2, hostname='localhost', description=None, last_communication=None, \
reboot_required=None, addresses=[], updates_count=0, boot_at=None, category='network_target_or_website', \
created_at='2021-02-02T16:31:39.000+01:00', cve_announcements_count=0, analyzed_at='2021-02-02T20:06:05.000+01:00', \
prioritized_cve_announcements_count=0, status='server_awaiting_analysis', os=None, \
environment=cbw_object(id=2, name='Medium', confidentiality_requirement='confidentiality_requirement_medium', \
integrity_requirement='integrity_requirement_medium', availability_requirement='availability_requirement_medium'), \
groups=[], compliance_groups=[])"""

            params = {'page': '1'}
            response = CBWApi(API_URL, API_KEY, SECRET_KEY).servers(params)
            assert isinstance(response, list) is True
            assert str(response[0]) == validate_server

    @staticmethod
    def test_server():
        """Tests for server method"""

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/server_ok.yaml'):
            response = CBWApi(API_URL, API_KEY, SECRET_KEY).server('4')
            assert response.category == 'server'
            assert response.cve_announcements[0].cve_code == 'CVE-2020-16044'

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/server_failed.yaml'):
            response = CBWApi(API_URL, API_KEY, SECRET_KEY).server('wrong_id')
            assert response is None

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
            response = client.delete_server('4')
            assert response is True

    @staticmethod
    def test_update_server():
        """Tests for server method"""

        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {'groups': [11, 12]}
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_server.yaml'):
            response = client.update_server('2', info)
            assert response is True

            response = client.update_server('', info)
            assert response is False

            response = client.update_server(None, info)
            assert response is False

            info = {'groups': [None], 'compliance_groups': [None]}
            with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_server_with_group_none.yaml'):
                response = client.update_server('2', info)
                assert response is True

    @staticmethod
    def test_agents():
        """Tests for method agents"""

        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/agents.yaml'):
            params = {'page': '1'}

            servers_validate = [
                "cbw_object(id=1, server_id=14, node_id=1, version='4.2', remote_ip='10.10.1.162', \
last_communication='2021-02-22T10:39:02.000+01:00')",
                "cbw_object(id=2, server_id=15, node_id=1, version='4.2', remote_ip='10.10.1.103', \
last_communication='2021-02-22T10:41:01.000+01:00')"
                ]

            response = client.agents(params)
            assert isinstance(response, list) is True
            assert str(response[0]) == servers_validate[0]
            assert str(response[1]) == servers_validate[1]

    @staticmethod
    def test_agent():
        """Tests for method agent"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/agent.yaml'):
            response = client.agent('2')

            assert str(response) == "cbw_object(id=2, server_id=15, node_id=1, version='4.2', remote_ip='10.10.1.103', \
last_communication='2021-02-22T10:41:01.000+01:00')"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/agent_wrong_id.yaml'):
            response = client.agent('wrong_id')

            assert response is None

    @staticmethod
    def test_delete_agent():
        """Tests for method delete_agent"""

        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_agent.yaml'):
            response = client.delete_agent('2')

            assert response is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_agent_wrong_id.yaml'):
            response = client.delete_agent('wrong_id')

            assert response is False

    @staticmethod
    def test_remote_accesses():
        """Tests for method remote_accesses"""

        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        remote_accesses_validate = [
            "cbw_object(id=10, type='CbwRam::RemoteAccess::Ssh::WithPassword', address='10.0.2.15', port=22, \
is_valid=False, last_error='Net::SSH::ConnectionTimeout', server_id=None, node_id=1)"]

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/remote_accesses.yaml'):
            params = {'page': '1'}
            response = client.remote_accesses(params)

            assert isinstance(response, list) is True
            assert str(response[0]) == remote_accesses_validate[0]
            assert response[2].type == 'CbwRam::RemoteAccess::Ssh::WithPassword'

    @staticmethod
    def test_create_remote_access():
        """Tests for method remote_access"""

        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {
            'type': 'CbwRam::RemoteAccess::Ssh::WithPassword',
            'address': 'X.X.X.X',
            'port': '22',
            'login': 'loginssh',
            'password': 'passwordssh',
            'key': '',
            'node_id': '1',
            'server_groups': 'test, production',
            'priv_password': '',
            'auth_password': '',
        }

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/create_remote_access.yaml'):
            response = client.create_remote_access(info)

            assert response.address == 'X.X.X.X', response.server_groups == ['test', 'production']
            assert response.type == 'CbwRam::RemoteAccess::Ssh::WithPassword'
            assert response.is_valid is None

        info['address'] = ''

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/create_remote_access_failed_without_address.yaml'):
            response = client.create_remote_access(info)

            assert response is False

    @staticmethod
    def test_remote_access():
        """Tests for method remote_access"""

        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/remote_access.yaml'):
            response = client.remote_access('16')

            assert response.address == 'X.X.X.X'
            assert response.type == 'CbwRam::RemoteAccess::Ssh::WithPassword'

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/remote_access_wrong_id.yaml'):
            response = client.remote_access('wrong_id')

            assert response is None

    @staticmethod
    def test_delete_remote_access():
        """Tests for method delete_remote_access"""

        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_remote_access.yaml'):
            response = client.delete_remote_access('16')

            assert response is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_remote_access_wrong_id.yaml'):
            response = client.delete_remote_access('wrong_id')

            assert response is False

    @staticmethod
    def test_update_remote_access():
        """Tests for update remote method"""

        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {
            'type': 'CbwRam::RemoteAccess::Ssh::WithPassword',
            'address': '10.10.10.228',
            'port': '22',
            'login': 'loginssh',
            'password': 'passwordssh',
            'key': '',
            'node': 'master',
        }

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_remote_access.yaml'):
            response = client.update_remote_access('10', info)

            assert response.address == '10.10.10.228', response.type == 'CbwRam::RemoteAccess::Ssh::WithPassword'

        info['address'] = '10.10.11.228'

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_remote_access_id_none.yaml'):
            response = client.update_remote_access(None, info)

            assert response is False

        info['type'] = ''

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_remote_access_without_type.yaml'):
            response = client.update_remote_access('10', info)

            assert response.type == 'CbwRam::RemoteAccess::Ssh::WithPassword'

    @staticmethod
    def test_cve_announcement():
        """Tests for method cve_announcement"""

        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/cve_announcement.yaml'):
            response = client.cve_announcement('CVE-2017-0146')
            assert response.cve_code == "CVE-2017-0146"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/cve_announcement_failed.yaml'):
            response = client.cve_announcement('wrong_id')

            assert response is None

    @staticmethod
    def test_group():
        """Tests for method groups"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        groups_validate = [
            "cbw_object(id=13, name='production', description='', color='#12afcb')",
            "cbw_object(id=14, name='Development', description='', color='#12afcb')"]

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/groups.yaml'):
            response = client.groups()

            assert str(response[2]) == groups_validate[0]
            assert str(response[3]) == groups_validate[1]

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/group.yaml'):
            response = client.group('13')

            assert str(response) == groups_validate[0]

        params = {
            "name": "test",
            "description": "test description",
        }

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/create_group.yaml'):
            response = client.create_group(params)

            assert response.name == "test", response.description == "test description"

        params["name"] = "test_change"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_group.yaml'):
            response = client.update_group('12', params)

            assert response.name == "test_change"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_group.yaml'):
            response = client.delete_group('12')

            assert response.name == "test_change"

    @staticmethod
    def test_deploy():
        """Tests for method test_deploy_remote_access"""

        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/test_deploy.yaml'):
            response = client.test_deploy_remote_access('15')
            assert str(response) == "cbw_object(id=15, type='CbwRam::RemoteAccess::Ssh::WithPassword', \
address='10.10.1.103', port=22, is_valid=None, last_error=None, server_id=13, node_id=1)"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/test_deploy_failed.yaml'):
            response = client.test_deploy_remote_access('wrong_id')

            assert response is None

    @staticmethod
    def test_users():
        """Tests for method users"""

        params = {'auth_provider': 'local_password'}
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/users.yaml'):
            response = CBWApi(API_URL, API_KEY, SECRET_KEY).users(params)

            assert str(response[0]) == "cbw_object(id=1, login='daniel@cyberwatch.fr', email='daniel@cyberwatch.fr', \
name='', firstname='', locale='fr', auth_provider='local_password', description='', server_groups=[])"

    @staticmethod
    def test_user():
        """Tests for method user"""

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/user.yaml'):
            response = CBWApi(API_URL, API_KEY, SECRET_KEY).user('1')

            assert str(response) == "cbw_object(id=1, login='daniel@cyberwatch.fr', email='daniel@cyberwatch.fr', \
name='', firstname='', locale='fr', auth_provider='local_password', description='', server_groups=[])"

    @staticmethod
    def test_cve_announcements():
        """Tests for method cve_announcements()"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)
        params = {
            'page': '1'
        }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/cve_announcements.yaml'):
            response = client.cve_announcements(params)

        assert response[0].cve_code == 'CVE-2012-1182'

    @staticmethod
    def test_update_cve_announcement():
        """Tests for method update_cve_announcement()"""

        client = CBWApi(API_URL, API_KEY, SECRET_KEY)
        cve_code = 'CVE-2019-16768'
        params = {
            'score_custom': '7',
            'access_complexity': 'access_complexity_low',
            'access_vector': 'access_vector_network',
            'availability_impact': 'availability_impact_none',
            'confidentiality_impact': 'confidentiality_impact_low',
            'integrity_impact': 'integrity_impact_low',
            'privilege_required': 'privilege_required_none',
            'scope': 'scope_changed',
            'user_interaction': 'user_interaction_required',
        }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_cve_announcement.yaml'):
            response = client.update_cve_announcement(cve_code, params)

        assert response.score_custom == 7.0, response.cvss_custom.scope == 'scope_changed'

    @staticmethod
    def test_delete_cve_announcement():
        """Tests for method delete_cve_announcement()"""

        client = CBWApi(API_URL, API_KEY, SECRET_KEY)
        cve_code = 'CVE-2019-16768'
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_cve_announcement.yaml'):
            response = client.delete_cve_announcement(cve_code)

        assert response.cve_code == 'CVE-2019-16768'

    @staticmethod
    def test_nodes():
        """Tests for method nodes()"""

        node_validate = [
            "cbw_object(id=1, name='master', created_at='2019-11-08T15:06:11.000+01:00', \
updated_at='2019-12-18T14:34:09.000+01:00')",
            "cbw_object(id=1, name='master', created_at='2019-11-08T15:06:11.000+01:00', \
updated_at='2019-12-16T14:17:29.000+01:00')"]

        client = CBWApi(API_URL, API_KEY, SECRET_KEY)
        params = {'page': '1'}
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/nodes.yaml'):
            response = client.nodes(params)

        assert str(response[0]) == node_validate[0]

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/node.yaml'):
            response = client.node('1')

            assert str(response) == node_validate[1]

        params = {'new_id': '1'}
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_node.yaml'):

            response = client.delete_node('2', params)

            assert response.id == 2

    @staticmethod
    def test_host():
        """Tests for method hosts"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        hosts_validate = [
            "cbw_object(id=8, target='172.18.0.13', category='linux', \
hostname='bb79e64ccd6e.dev_default', cve_announcements_count=0, created_at='2019-11-14T11:58:50.000+01:00', \
updated_at='2019-12-16T16:45:42.000+01:00', node_id=1, server_id=5, status='server_update_init', \
technologies=[], security_issues=[], cve_announcements=[], scans=[])",
            "cbw_object(id=12, target='5.5.5.5', category='linux', hostname=None, cve_announcements_count=0, \
created_at='2019-12-17T14:28:00.000+01:00', updated_at='2019-12-17T14:28:00.000+01:00', node_id=1, \
server_id=7, status='server_update_init', technologies=[], security_issues=[], cve_announcements=[], scans=[])"]

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/hosts.yaml'):
            response = client.hosts()

        assert len(response) == 4, str(response[0]) == hosts_validate[0]

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/host.yaml'):
            response = client.host('12')

            assert str(response) == hosts_validate[1]

        params = {
            "target": "192.168.1.2",
            "node_id": "1"
        }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/create_host.yaml'):
            response = client.create_host(params)

            assert response.target == "192.168.1.2", response.node_id == 1

        params["category"] = "other"
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_host.yaml'):
            response = client.update_host('1', params)

        assert response.category == "other", response.node_id == 1

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_host.yaml'):
            response = client.delete_host('1')

            assert response.target == '10.10.1.186'

    @staticmethod
    def test_update_server_cve():
        """Tests for server method"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {
            "comment": "test"
        }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_server_cve.yaml'):
            response = client.update_server_cve('9', "CVE-2020-28928", info)
            assert response.cve_announcements[1].comment == 'test'

        info = {
            "ignored": "true",
            "comment": "test-ignore"
        }
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_server_cve_ignored.yaml'):
            response = client.update_server_cve('9', "CVE-2020-28928", info)
            assert len(response.cve_announcements) == 1


    @staticmethod
    def test_security_issues():
        """Tests for method security_issues"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        security_issues_validate = [
            "cbw_object(id=28, type='SecurityIssues::Custom', sid='test', level='level_info', \
title='test', description='test')",
            "cbw_object(id=29, type='SecurityIssues::Custom', sid='test2', level='level_low', \
title='test2', description='test2')"]

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/security_issues.yaml'):
            params = {
                'page': '1'
            }
            response = client.security_issues(params)
            assert isinstance(response, list) is True
            assert str(response[0]) == security_issues_validate[0]
            assert str(response[1]) == security_issues_validate[1]

    @staticmethod
    def test_create_security_issue():
        """Tests for method security_issue"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {
            "description": "Test",
            "level": "level_critical",
            "score": "5",
            "type": "SecurityIssues::Custom",
            "sid": "test3"
        }

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/create_security_issue.yaml'):
            response = client.create_security_issue(info)

            assert response.level == "level_critical"
            assert response.description == "Test"

    @staticmethod
    def test_update_security_issue():
        """Tests for update remote method"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {
            "description": "Test update",
            "level": "level_low",
            "score": "6",
        }

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_security_issue.yaml'):
            response = client.update_security_issue('30', info)

            assert response.description == "Test update"

        info["level"] = "level_test"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_security_issue_wrong_level.yaml'):
            response = client.update_security_issue("30", info)

            assert response is None

    @staticmethod
    def test_delete_security_issue():
        """Tests for method delete_security_issue"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_security_issue.yaml'):
            response = client.delete_security_issue('30')
            assert str(response) == "cbw_object(id=30, type='SecurityIssues::Custom', sid='test3', level='level_low', \
title=None, description='Test update', servers=[], cve_announcements=[])"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_security_issue_wrong_id.yaml'):
            response = client.delete_security_issue('wrong_id')
            assert response is None

    @staticmethod
    def test_fetch_airgapped_scripts():
        """Tests for method to fetch air gapped scanning scripts"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/fetch_airgapped_script.yaml'):
            response = client.fetch_airgapped_script('1')
            assert response.version == '47c8367e1c92d50fad8894362f5c09e9bfe65e712aab2d23ffbb61e354e270dd'

    @staticmethod
    def test_compliance_servers():
        """Tests for method compliance_servers"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        validate_compliance_asset = "cbw_object(id=2, hostname='fc14251fc5b7', description=None, \
last_communication='2020-08-05T09:57:02.000+02:00', reboot_required=False, boot_at='2020-07-28T15:12:56.000+02:00', \
category='server', created_at='2020-08-04T10:54:58.000+02:00', compliance_rules_count=0, compliance_rules_failed_count=0, \
compliance_rules_succeed_count=0, status='gen_idle', os=cbw_object(key='ubuntu_2004_64', name='Ubuntu 20.04 LTS', \
arch='x86_64', eol='2025-04-01T02:00:00.000+02:00', short_name='Ubuntu 20.04', type='Os::Ubuntu'), \
environment=cbw_object(id=2, name='Medium', default=True, confidentiality_requirement='confidentiality_requirement_medium', \
integrity_requirement='integrity_requirement_medium', availability_requirement='availability_requirement_medium', \
threshold=7.5, created_at='2020-08-03T17:47:02.237+02:00', updated_at='2020-08-03T17:47:02.237+02:00'), \
groups=[cbw_object(id=12, name='computers_factory_4X', description=None, color='#12AFCB', \
created_at='2020-08-04T10:54:58.000+02:00', updated_at='2020-08-04T10:54:58.000+02:00'), \
cbw_object(id=14, name='dead', description=None, color='#12AFCB', created_at='2020-08-05T11:48:51.000+02:00', \
updated_at='2020-08-05T11:48:51.000+02:00'), cbw_object(id=18, name='agent', description=None, color='#12AFCB', \
created_at='2020-08-13T15:57:45.000+02:00', updated_at='2020-08-13T15:57:45.000+02:00')], compliance_groups=[])"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/compliance_servers.yaml'):
            param = {"environment_id":"2"}
            response = client.compliance_servers(param)
            assert len(response) == 27
            assert isinstance(response, list) is True
            assert str(response[0]) == validate_compliance_asset

    @staticmethod
    def test_compliance_server():
        """Tests for method compliance_server"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        validate_compliance_asset = "cbw_object(id=2, hostname='fc14251fc5b7', description=None, \
last_communication='2020-08-05T09:57:02.000+02:00', reboot_required=False, boot_at='2020-07-28T15:12:56.000+02:00', \
category='server', created_at='2020-08-04T10:54:58.000+02:00', compliance_rules_count=0, \
compliance_rules_failed_count=0, compliance_rules_succeed_count=0, status='gen_idle', rules=[], \
os=cbw_object(key='ubuntu_2004_64', name='Ubuntu 20.04 LTS', arch='x86_64', eol='2025-04-01T02:00:00.000+02:00', \
short_name='Ubuntu 20.04', type='Os::Ubuntu'), environment=cbw_object(id=2, name='Medium', default=True, \
confidentiality_requirement='confidentiality_requirement_medium', integrity_requirement='integrity_requirement_medium', \
availability_requirement='availability_requirement_medium', threshold=7.5, created_at='2020-08-03T17:47:02.237+02:00', \
updated_at='2020-08-03T17:47:02.237+02:00'), groups=[cbw_object(id=12, name='computers_factory_4X', description=None, \
color='#12AFCB', created_at='2020-08-04T10:54:58.000+02:00', updated_at='2020-08-04T10:54:58.000+02:00'), \
cbw_object(id=14, name='dead', description=None, color='#12AFCB', created_at='2020-08-05T11:48:51.000+02:00', \
updated_at='2020-08-05T11:48:51.000+02:00'), cbw_object(id=18, name='agent', description=None, color='#12AFCB', \
created_at='2020-08-13T15:57:45.000+02:00', updated_at='2020-08-13T15:57:45.000+02:00')], compliance_groups=[])"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/compliance_server.yaml'):
            response = client.compliance_server("2")
            assert str(response) == validate_compliance_asset

    @staticmethod
    def test_recheck_rules():
        """Tests for method recheck_rules"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        validate_recheck_rules = "cbw_object(id=2, hostname='fc14251fc5b7', description=None, \
last_communication='2020-08-05T09:57:02.000+02:00', reboot_required=False, boot_at='2020-07-28T15:12:56.000+02:00', \
category='server', created_at='2020-08-04T10:54:58.000+02:00', compliance_rules_count=0, compliance_rules_failed_count=0, \
compliance_rules_succeed_count=0, status='gen_idle', rules=[], os=cbw_object(key='ubuntu_2004_64', name='Ubuntu 20.04 LTS', \
arch='x86_64', eol='2025-04-01T02:00:00.000+02:00', short_name='Ubuntu 20.04', type='Os::Ubuntu'), \
environment=cbw_object(id=2, name='Medium', default=True, confidentiality_requirement='confidentiality_requirement_medium', \
integrity_requirement='integrity_requirement_medium', availability_requirement='availability_requirement_medium', threshold=7.5, \
created_at='2020-08-03T17:47:02.237+02:00', updated_at='2020-08-03T17:47:02.237+02:00'), groups=[cbw_object(id=12, \
name='computers_factory_4X', description=None, color='#12AFCB', created_at='2020-08-04T10:54:58.000+02:00', \
updated_at='2020-08-04T10:54:58.000+02:00'), cbw_object(id=14, name='dead', description=None, color='#12AFCB', \
created_at='2020-08-05T11:48:51.000+02:00', updated_at='2020-08-05T11:48:51.000+02:00'), cbw_object(id=18, name='agent', \
description=None, color='#12AFCB', created_at='2020-08-13T15:57:45.000+02:00', updated_at='2020-08-13T15:57:45.000+02:00')], \
compliance_groups=[])"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/recheck_rules.yaml'):
            response = client.recheck_rules("2")
            assert str(response) == validate_recheck_rules

    @staticmethod
    def test_compliance_rules():
        """Tests for method compliance_rules"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/compliance_rules.yaml'):
            response = client.compliance_rules()
            assert(len(response)) == 4646
            assert(response[0].id) == 1
            assert isinstance(response, list) is True

    @staticmethod
    def test_compliance_rule():
        """Tests for method compliance_rule"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        validate_compliance_rule = """cbw_object(id=6891, audit='Verify cron is enabledchecks:=[{"order" = 1,\
"content" = "systemctl is-enabled cron","success" = "enabled","failure" = "disabled"},{"order" = 2,\
"content" = "service cron status","success" = "active","failure" = "disabled"}]', code='SBP-Custom-001-cron', \
description='The cron daemon is used to execute batch jobs on the system.', name='Ensure cron daemon is enabled', \
rationale='While there may not be user jobs that need to be run on the system, the system does have maintenance jobs \
that may include security monitoring that have to run, and cron is used to execute them.', \
remediation='systemctl --now enable cron', level='minimal', require_sudo=None, type='CbwCompliance::Rules::Custom', \
created_at='2020-09-30T09:51:26.000+02:00', updated_at='2020-09-30T09:51:26.000+02:00', published_at=None, \
last_modified_at=None, reference=None, equation='(1 && 2)', os=[cbw_object(key='ubuntu_2004_64')], servers=[], \
rule_groups=[], checks=[])"""

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/compliance_rule.yaml'):
            response = client.compliance_rule("6891")
            assert str(response) == validate_compliance_rule

    @staticmethod
    def test_create_compliance_rule():
        """Tests for method create_compliance_rule"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {
        "audit": "rule audit",
        "code": "SBP-Custom-001",
        "description": "rule description",
        "equation": "(1 && 2)",
        "name": "rule name",
        "rationale": "rule rationale",
        "remediation": "rule remediation",
        "checks": [
                {
                    "order": 1,
                    "content": "check content",
                    "success": "regex success",
                    "failure": "regex failure"
                },
                {
                    "order": 2,
                    "content": "check content",
                    "success": "regex success",
                    "failure": "regex failure"
                }
            ],
            "os": ["ubuntu_2004_64"]
        }

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/create_compliance_rule.yaml'):
            response = client.create_compliance_rule(info)
            assert response.code == "SBP-Custom-001"
            assert response.description == "rule description"

    @staticmethod
    def test_update_compliance_rule():
        """Tests for method update_compliance_rule"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {"audit": "New audit for this rule", "description": "new description"}
        rule_id = "6891"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_compliance_rule.yaml'):
            response = client.update_compliance_rule(rule_id, info)
            assert response is True

            rule_updated = client.compliance_rule(rule_id)
            assert rule_updated.audit == "New audit for this rule"
            assert rule_updated.description == "new description"

    @staticmethod
    def test_delete_compliance_rule():
        """Tests for method delete_compliance_rule"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_compliance_rule_OK.yaml'):
            response = client.delete_compliance_rule("6891")
            assert response is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_compliance_rule_KO.yaml'):
            response = client.delete_compliance_rule("6890")
            assert response is False

    @staticmethod
    def test_recheck_servers():
        """Tests for method recheck_servers"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)
        rule_id = "6885"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/recheck_servers.yaml'):
            response = client.recheck_servers(rule_id)
            assert str(response.id) == rule_id
            assert isinstance(response.servers, list) is True
            assert len(response.servers) == 5

    @staticmethod
    def test_docker_images():
        """Tests for method docker_images"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        docker_images_validate = [
            "cbw_object(id=1, image_name='library/alpine', image_tag='latest', \
docker_registry_id=1, docker_engine_id=4, node_id=1, server_id=6)"]

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/docker_images.yaml'):
            params = {
                'page': '1'
            }
            response = client.docker_images(params)
            assert isinstance(response, list) is True
            assert str(response[0]) == docker_images_validate[0], str(
                response[0]) == docker_images_validate[0]

    @staticmethod
    def test_create_docker_image():
        """Tests for method docker_image"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {
            "image_name": "library/debian",
            "image_tag": "latest",
            "docker_registry_id": "1",
            "docker_engine_id": "4",
            "node_id": "1",
        }

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/create_docker_image.yaml'):
            response = client.create_docker_image(info)

            assert str(response) == "cbw_object(id=6, image_name='library/debian', image_tag='latest', \
docker_registry_id=1, docker_engine_id=4, node_id=1, server_id=None)"

    @staticmethod
    def test_update_docker_image():
        """Tests for update remote method"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {
            "image_tag": "bullseye",
        }

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_docker_image.yaml'):
            response = client.update_docker_image('3', info)

            assert response is True

    @staticmethod
    def test_delete_docker_image():
        """Tests for method delete_docker_image"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_docker_image.yaml'):
            response = client.delete_docker_image('3')
            assert response is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_docker_image_wrong_id.yaml'):
            response = client.delete_docker_image('wrong_id')
            assert response is False

    @staticmethod
    def test_assets():
        """Tests for method assets"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        assets_validate = ["cbw_object(id=2, hostname='localhost', description=None, last_communication=None, \
reboot_required=None, boot_at=None, category='network_target_or_website', created_at='2021-02-02T16:31:39.000+01:00', \
environment=cbw_object(id=2, name='Medium', confidentiality_requirement='confidentiality_requirement_medium', \
integrity_requirement='integrity_requirement_medium', availability_requirement='availability_requirement_medium'), os=None, \
groups=[])", "cbw_object(id=3, hostname='Linux', description=None, last_communication=None, reboot_required=None, \
boot_at=None, category='server', created_at='2021-02-03T11:49:28.000+01:00', environment=cbw_object(id=2, name='Medium', \
confidentiality_requirement='confidentiality_requirement_medium', integrity_requirement='integrity_requirement_medium', \
availability_requirement='availability_requirement_medium'), os=cbw_object(key='ubuntu_2004_64', name='Ubuntu 20.04 LTS', \
arch='x86_64', eol='2025-04-01T02:00:00.000+02:00', short_name='Ubuntu 20.04', type='Os::Ubuntu'), \
groups=[cbw_object(id=11, name='t4est', description='', color='#12afcb')]), cbw_object(id=4, hostname='Linux2', description=None, \
last_communication=None, reboot_required=None, boot_at=None, category='server', created_at='2021-02-03T11:49:46.000+01:00', \
environment=cbw_object(id=2, name='Medium', confidentiality_requirement='confidentiality_requirement_medium', \
integrity_requirement='integrity_requirement_medium', availability_requirement='availability_requirement_medium'), \
os=cbw_object(key='ubuntu_2004_64', name='Ubuntu 20.04 LTS', arch='x86_64', eol='2025-04-01T02:00:00.000+02:00', short_name='Ubuntu 20.04', \
type='Os::Ubuntu'), groups=[cbw_object(id=11, name='t4est', description='', color='#12afcb')]), cbw_object(id=9, hostname='library/alpine:latest', \
description=None, last_communication=None, reboot_required=None, boot_at=None, category='docker_image', created_at='2021-02-12T11:26:46.000+01:00', \
environment=cbw_object(id=2, name='Medium', confidentiality_requirement='confidentiality_requirement_medium', integrity_requirement='integrity_requirement_medium', \
availability_requirement='availability_requirement_medium'), os=cbw_object(key='alpine_linux_64', name='Alpine Linux', arch='x86_64', eol=None, \
short_name='Alpine Linux', type='Os::Alpine'), groups=[]), cbw_object(id=11, hostname='library/debian:latest', description=None, last_communication=None, \
reboot_required=None, boot_at=None, category='docker_image', created_at='2021-02-12T11:42:52.000+01:00', environment=cbw_object(id=2, name='Medium', \
confidentiality_requirement='confidentiality_requirement_medium', integrity_requirement='integrity_requirement_medium', \
availability_requirement='availability_requirement_medium'), os=cbw_object(key='debian_10_64', name='Debian 10 (Buster)', arch='x86_64', \
eol='2022-12-31T01:00:00.000+01:00', short_name='Debian 10', type='Os::Debian'), groups=[])"""]


        with vcr.use_cassette('spec/fixtures/vcr_cassettes/assets.yaml'):
            response = client.assets()
            assert str(response[0]) == assets_validate[0]

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/asset.yaml'):
            response = client.asset('3')

            asset_validate = """cbw_object(id=3, hostname='Linux', description=None, last_communication=None, \
reboot_required=None, boot_at=None, category='server', created_at='2021-02-03T11:49:28.000+01:00', \
environment=cbw_object(id=2, name='Medium', confidentiality_requirement='confidentiality_requirement_medium', \
integrity_requirement='integrity_requirement_medium', \
availability_requirement='availability_requirement_medium'), os=cbw_object(key='ubuntu_2004_64', \
name='Ubuntu 20.04 LTS', arch='x86_64', eol='2025-04-01T02:00:00.000+02:00', short_name='Ubuntu 20.04', \
type='Os::Ubuntu'), groups=[cbw_object(id=11, name='t4est', description='', color='#12afcb')], \
packages=[cbw_object(vendor=None, product='firefox', type='Packages::Deb', \
version='80.0.1+build1-0ubuntu0.20.04.1')], applications=[])"""

            assert str(response) == asset_validate

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_asset.yaml'):
            response = client.delete_asset('3')

            assert response.hostname == 'Linux'

    @staticmethod
    def test_applicative_scans():
        """Tests for method applicative_scans"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        applicative_scans_validate = ["cbw_object(id=1, node_id=1, target='fenrisl.com', server_id=1)"]

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/applicative_scans.yaml'):
            params = {
                'page': '1'
            }
            response = client.applicative_scans(params)
            assert isinstance(response, list) is True
            assert str(response[0]) == applicative_scans_validate[0], str(response[0]) == applicative_scans_validate[0]

    @staticmethod
    def test_create_applicative_scan():
        """Tests for method applicative_scan"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {
            "target": "127.0.0.1",
            "node_id": "1"
        }

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/create_applicative_scan.yaml'):
            response = client.create_applicative_scan(info)

            assert str(response) == "cbw_object(id=2, node_id=1, target='127.0.0.1', server_id=2)"

    @staticmethod
    def test_update_applicative_scan():
        """Tests for update remote method"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        info = {
            "target": "localhost",
        }

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_applicative_scan.yaml'):
            response = client.update_applicative_scan('2', info)

            assert response is True

        info["target"] = "invalid@target"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/update_applicative_scan_wrong_target.yaml'):
            response = client.update_applicative_scan("2", info)

            assert response is False

    @staticmethod
    def test_delete_applicative_scan():
        """Tests for method delete_applicative_scan"""
        client = CBWApi(API_URL, API_KEY, SECRET_KEY)

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_applicative_scan.yaml'):
            response = client.delete_applicative_scan('1')
            assert response is True

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/delete_applicative_scan_wrong_id.yaml'):
            response = client.delete_applicative_scan('wrong_id')
            assert response is False
