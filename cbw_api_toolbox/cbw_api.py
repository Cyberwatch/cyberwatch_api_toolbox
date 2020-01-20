"""Module used to communicate with the CBW API"""

import json
import logging
import sys

from urllib.parse import urlparse
from urllib.parse import parse_qs
from collections import defaultdict
import requests
from requests.exceptions import ProxyError, SSLError, RetryError, InvalidHeader, MissingSchema
from urllib3.exceptions import NewConnectionError, MaxRetryError

from cbw_api_toolbox.__routes__ import ROUTE_CVE_ANNOUNCEMENTS
from cbw_api_toolbox.__routes__ import ROUTE_GROUPS
from cbw_api_toolbox.__routes__ import ROUTE_HOSTS
from cbw_api_toolbox.__routes__ import ROUTE_NODES
from cbw_api_toolbox.__routes__ import ROUTE_PING
from cbw_api_toolbox.__routes__ import ROUTE_REMOTE_ACCESSES
from cbw_api_toolbox.__routes__ import ROUTE_SERVERS
from cbw_api_toolbox.__routes__ import ROUTE_USERS
from cbw_api_toolbox.cbw_auth import CBWAuth
from cbw_api_toolbox.cbw_objects.cbw_server import CBWCve
from cbw_api_toolbox.cbw_objects.cbw_group import CBWGroup
from cbw_api_toolbox.cbw_objects.cbw_host import CBWHost
from cbw_api_toolbox.cbw_objects.cbw_node import CBWNode
from cbw_api_toolbox.cbw_objects.cbw_remote_access import CBWRemoteAccess
from cbw_api_toolbox.cbw_objects.cbw_server import CBWServer
from cbw_api_toolbox.cbw_objects.cbw_users import CBWUsers
from cbw_api_toolbox.cbw_parser import CBWParser


class CBWApi: # pylint: disable=R0904
    """Class used to communicate with the CBW API"""

    def __init__(self, api_url, api_key, secret_key, verify_ssl=False):
        self.api_url = api_url
        self.api_key = api_key
        self.secret_key = secret_key

        self.verify_ssl = verify_ssl
        self.logger = logging.getLogger(self.__class__.__name__)

    def _build_route(self, params):
        return "{0}{1}".format(self.api_url, '/'.join(params))

    def _request(self, verb, payloads, body_params=None):
        route = self._build_route(payloads)

        if body_params is not None:
            body_params = json.dumps(body_params)

        try:
            return requests.request(
                verb,
                route,
                data=body_params,
                auth=CBWAuth(self.api_key, self.secret_key),
                verify=self.verify_ssl)

        except (ConnectionError, ProxyError, SSLError, NewConnectionError, RetryError,
                InvalidHeader, MaxRetryError):
            self.logger.exception("An error occurred when requesting {}".format(route))

        except MissingSchema:
            self.logger.error("An error occurred, please check your API_URL.")
            sys.exit(-1)

    def _get_pages(self, verb, route, params, model):
        """ Get one or more pages for a method using api v3 pagination """
        response_list = []

        if 'per_page' not in params:
            params['per_page'] = 100

        if 'page' in params:
            response = self._request(verb, route, params)
            if response.status_code != 200:
                logging.error("Error::{}".format(response.text))
                return None
            return CBWParser().parse_response(model, response)

        response = self._request(verb, route, params)

        if response.status_code != 200:
            logging.error("Error::{}".format(response.text))
            return None

        response_list.extend(CBWParser().parse_response(model, response))

        while 'next' in response.links:
            next_url = urlparse(response.links['next']['url'])
            params['page'] = parse_qs(next_url .query)['page'][0]
            response = self._request(verb, route, params)
            response_list.extend(CBWParser().parse_response(model, response))
        return response_list

    @staticmethod
    def verif_response(response):
        """Check the response status code"""
        if response.status_code >= 200 and response.status_code <= 299:
            logging.debug("response server OK::{}".format(response.text))
            return True

        logging.error("response server KO::{}".format(response.text))
        return False

    def ping(self):
        """GET request to /api/v3/ping then check uuid value"""
        response = self._request("GET", [ROUTE_PING])

        if response.status_code == 200:
            logging.info("OK")
            return True
        logging.error("FAILED")
        return False

    def servers(self, params=defaultdict()):
        """GET request to /api/v3/servers to get all servers"""
        response = self._get_pages("GET", [ROUTE_SERVERS], params, CBWServer)

        return response

    def server(self, server_id):
        """GET request to /api/v3/server/{server_id} to get all informations
        about a specific server"""
        response = self._request("GET", [ROUTE_SERVERS, server_id])
        if response.status_code != 200:
            logging.error("Error server id::{}".format(response.text))
            return None

        return CBWParser().parse_response(CBWServer, response)

    def update_server(self, server_id, info):
        """PATCH request to /api/v3/servers/SERVER_ID to update the groups of a server"""
        if server_id:
            response = self._request("PATCH", [ROUTE_SERVERS, server_id], info)

            logging.debug("Update server with: {}".format(info))

            return self.verif_response(response)

        logging.error("No server id for update")
        return False

    def delete_server(self, server_id):
        """DELETE request to /api/v3/servers/SERVER_ID to delete a specific server"""
        if server_id:
            logging.debug("Deleting {}".format(server_id))
            response = self._request("DELETE", [ROUTE_SERVERS, server_id])
            return self.verif_response(response)

        logging.error("No server id specific for delete")
        return False

    def update_server_cve(self, server_id, cve_code, params=defaultdict()):
        """PUT request to /api/v3/server/<server_id>/cve_announcements/<cve_code> to update a server cve"""
        response = self._request("PUT", [ROUTE_SERVERS, server_id, "cve_announcements", cve_code], params)
        if response.status_code != 200:
            logging.error("Error::{}".format(response.text))
            return None

        return CBWParser().parse_response(CBWServer, response)

    def remote_accesses(self, params=defaultdict()):
        """GET request to /api/v3/remote_accesses to get all servers"""
        response = self._get_pages("GET", [ROUTE_REMOTE_ACCESSES], params, CBWRemoteAccess)

        return response

    def create_remote_access(self, info):
        """"POST request to /api/v3/remote_accesses to create a specific remote access"""
        if info:
            response = self._request("POST", [ROUTE_REMOTE_ACCESSES], {
                "type": info["type"],
                "address": info["address"],
                "port": info["port"],
                "login": info["login"],
                "password": info.get("auth_password") or info.get("password"),
                "key": info.get("priv_password") or info.get("key"),
                "node_id": info["node_id"],
                "server_groups" : info.get("server_groups", "")
            })
            logging.debug("Create connexion remote access::{}".format(response.text))

        if self.verif_response(response):
            logging.info('remote access successfully created {}'.format(info["address"]))
            return CBWParser().parse_response(CBWRemoteAccess, response)

        logging.error("Error create connection remote access")
        return False

    def remote_access(self, remote_access_id):
        """GET request to /api/v3/remote_accesses/{remote_access_id} to get all informations
        about a specific remote access"""
        response = self._request("GET", [ROUTE_REMOTE_ACCESSES, remote_access_id])

        if response.status_code != 200:
            logging.error("error remote_access_id::{}".format(response.text))
            return None

        return CBWParser().parse_response(CBWRemoteAccess, response)

    def delete_remote_access(self, remote_access_id):
        """DELETE request to /api/v3/remote_access/{remote_id} to delete a specific remote access"""
        if remote_access_id:
            logging.debug("Deleting remote access {}".format(remote_access_id))
            response = self._request("DELETE", [ROUTE_REMOTE_ACCESSES, remote_access_id])
            return self.verif_response(response)

        logging.error("No remote_access_id for delete")
        return False

    def update_remote_access(self, remote_access_id, info):
        """PATCH request to /api/v3/remote_accesses/{remote_id} to update a remote access"""
        if remote_access_id and info:
            response = self._request("PATCH", [ROUTE_REMOTE_ACCESSES, remote_access_id], info)
            logging.debug("Update remote access::{}".format(response.text))
            return CBWParser().parse_response(CBWRemoteAccess, response)

        logging.error("Error update remote access")
        return False

    def cve_announcement(self, cve_code):
        """GET request to /api/v3/cve_announcements/{cve_code} to get all informations
        about a specific cve_announcement"""
        response = self._request("GET", [ROUTE_CVE_ANNOUNCEMENTS, cve_code])
        if response.status_code != 200:
            logging.error("Error server id::{}".format(response.text))
            return None

        return CBWParser().parse_response(CBWCve, response)

    def cve_announcements(self, params=defaultdict()):
        """GET request to /api/v3/cve_announcements to get a list of cve_announcement"""
        response = self._get_pages("GET", [ROUTE_CVE_ANNOUNCEMENTS], params, CBWCve)

        return response

    def groups(self, params=defaultdict()):
        """GET request to /api/v3/groups to get a list of groups"""
        response = self._get_pages("GET", [ROUTE_GROUPS], params, CBWGroup)

        return response

    def group(self, group_id):
        """GET request to /api/v3/groups/<group_id> to get a specific group"""
        response = self._request("GET", [ROUTE_GROUPS, group_id])
        if response.status_code != 200:
            logging.error("Error::{}".format(response.text))
            return None

        return CBWParser().parse_response(CBWGroup, response)

    def create_group(self, params):
        """POST request to /api/v3/groups to create a group"""
        response = self._request("POST", [ROUTE_GROUPS], params)
        if response.status_code != 201:
            logging.error("Error::{}".format(response.text))
            return None

        return CBWParser().parse_response(CBWGroup, response)

    def update_group(self, group_id, params=defaultdict()):
        """PUT request to /api/v3/groups/<group_id> to update a group"""
        response = self._request("PUT", [ROUTE_GROUPS, group_id], params)
        if response.status_code != 200:
            logging.error("Error::{}".format(response.text))
            return None

        return CBWParser().parse_response(CBWGroup, response)

    def delete_group(self, group_id):
        """DELETE request to /api/v3/groups/<group_id> to delete a group"""
        response = self._request("DELETE", [ROUTE_GROUPS, group_id])
        if response.status_code != 200:
            logging.error("Error::{}".format(response.text))
            return None

        return CBWParser().parse_response(CBWGroup, response)

    def test_deploy_remote_access(self, remote_access_id):
        """POST request to /api/v3/remote_accesses/:id/test_deploy to test an agentless deployment"""
        response = self._request("PUT", [ROUTE_REMOTE_ACCESSES, remote_access_id, 'test_deploy'])
        if response.status_code != 200:
            logging.error("Error::{}".format(response.text))
            return None
        return CBWParser().parse_response(CBWRemoteAccess, response)

    def users(self, params=defaultdict()):
        """GET request to /api/v3/users to get a list of users"""
        response = self._get_pages("GET", [ROUTE_USERS], params, CBWUsers)

        return response

    def user(self, user_id):
        """GET request to /api/v3/users/<id> to get a specific user"""
        response = self._request("GET", [ROUTE_USERS, user_id])

        if response.status_code != 200:
            logging.error("Error::{}".format(response.text))
            return None

        return CBWParser().parse_response(CBWUsers, response)

    def nodes(self, params=defaultdict()):
        """GET request to /api/v3/nodes to get a list of all nodes"""
        response = self._get_pages("GET", [ROUTE_NODES], params, CBWNode)

        return response

    def node(self, node_id):
        """GET request to /api/v3/nodes/<node_id> to get a list of all nodes"""
        response = self._request("GET", [ROUTE_NODES, node_id])
        if response.status_code != 200:
            logging.error("Error::{}".format(response.text))
            return None

        return CBWParser().parse_response(CBWNode, response)

    def delete_node(self, node_id, new_node_id):
        """DELETE request to /api/v3/nodes/<node_id> to delete a node and transfer the data to another one"""
        response = self._request("DELETE", [ROUTE_NODES, node_id], new_node_id)
        if response.status_code != 200:
            logging.error("Error::{}".format(response.text))
            return None

        return CBWParser().parse_response(CBWNode, response)

    def hosts(self, params=defaultdict()):
        """GET request to /api/v3/hosts to get a list of all hosts"""
        response = self._get_pages("GET", [ROUTE_HOSTS], params, CBWHost)

        return response

    def host(self, host_id):
        """GET request to /api/v3/hosts/<host_id> to get a specific host"""
        response = self._request("GET", [ROUTE_HOSTS, host_id])
        if response.status_code != 200:
            logging.error("Error::{}".format(response.text))
            return None

        return CBWParser().parse_response(CBWHost, response)

    def create_host(self, params):
        """POST request to /api/v3/hosts to create a host"""
        response = self._request("POST", [ROUTE_HOSTS], params)
        if response.status_code != 201:
            logging.error("Error::{}".format(response.text))
            return None

        return CBWParser().parse_response(CBWHost, response)

    def update_host(self, host_id, params=defaultdict()):
        """PUT request to /api/v3/hosts/<host_id> to update a host"""
        response = self._request("PUT", [ROUTE_HOSTS, host_id], params)
        if response.status_code != 200:
            logging.error("Error::{}".format(response.text))
            return None

        return CBWParser().parse_response(CBWHost, response)

    def delete_host(self, host_id):
        """DELETE request to /api/v3/hosts/<host_id> to delete a host"""
        response = self._request("DELETE", [ROUTE_HOSTS, host_id])
        if response.status_code != 200:
            logging.error("Error::{}".format(response.text))
            return None

        return CBWParser().parse_response(CBWHost, response)
