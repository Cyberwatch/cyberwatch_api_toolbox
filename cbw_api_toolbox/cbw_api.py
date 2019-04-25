"""Module used to communicate with the CBW API"""

import json
import logging
import sys

import requests
from requests.exceptions import ProxyError, SSLError, RetryError, InvalidHeader, MissingSchema
from urllib3.exceptions import NewConnectionError, MaxRetryError

from cbw_api_toolbox import API_DEFAULT_URL
from cbw_api_toolbox.__routes__ import ROUTE_SERVERS, ROUTE_PING, ROUTE_REMOTE_ACCESSES
from cbw_api_toolbox.cbw_auth import CBWAuth
from cbw_api_toolbox.cbw_objects.cbw_server import CBWServer
from cbw_api_toolbox.cbw_objects.cbw_remote_access import CBWRemoteAccess
from cbw_api_toolbox.cbw_parser import CBWParser


class CBWApi:
    """Class used to communicate with the CBW API"""

    def __init__(self, api_url, api_key, secret_key, verify_ssl=False):
        self.api_url = api_url + API_DEFAULT_URL
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

    @staticmethod
    def verif_response(response):
        """Check the response status code"""
        if response.status_code >= 200 and response.status_code <= 299:
            logging.debug("response server OK::{}".format(response.text))
            return True

        logging.error("response server KO::{}".format(response.text))
        return False

    def ping(self):
        """GET request to /api/v2/ping then check uuid value"""
        response = self._request("GET", [ROUTE_PING])

        if response.status_code == 200:
            logging.info("OK")
            return True
        logging.error("FAILED")
        return False

    def servers(self):
        """GET request to /api/v2/servers to get all servers"""
        response = self._request("GET", [ROUTE_SERVERS])

        return CBWParser().parse_response(CBWServer, response)

    def server(self, server_id):
        """GET request to /api/v2/server/{server_id} to get all informations
        about a specific server"""
        response = self._request("GET", [ROUTE_SERVERS, server_id])
        if response.status_code != 200:
            logging.error("Error server id::{}".format(response.text))
            return None

        return CBWParser().parse_response(CBWServer, response)

    def update_server(self, server_id, info):
        """PATCH request to /api/v2/servers/SERVER_ID to update the groups of a server"""
        if server_id:
            params = {
                'groups': info["groups"],
                'compliance_groups': info["compliance_groups"]
            }
            response = self._request("PATCH", [ROUTE_SERVERS, server_id], params)

            logging.debug("Update server with: {}".format(params))

            return self.verif_response(response)

        logging.error("No server id for update")
        return False

    def delete_server(self, server_id):
        """DELETE request to /api/v2/servers/SERVER_ID to delete a specific server"""
        if server_id:
            logging.debug("Deleting {}".format(server_id))
            response = self._request("DELETE", [ROUTE_SERVERS, server_id])
            return self.verif_response(response)

        logging.error("No server id specific for delete")
        return False

    def remote_accesses(self):
        """GET request to /api/v2/remote_accesses to get all servers"""
        response = self._request("GET", [ROUTE_REMOTE_ACCESSES])
        return CBWParser().parse_response(CBWRemoteAccess, response)

    def create_remote_access(self, info):
        """"POST request to /api/v2/remote_accesses to create a specific remote access"""
        if info:
            response = self._request("POST", [ROUTE_REMOTE_ACCESSES], {
                "type": info["type"],
                "address": info["address"],
                "port": info["port"],
                "login": info["login"],
                "password": info["password"],
                "key": info["key"],
                "node": info["node"]
            })
            logging.debug("Create connexion remote access::{}".format(response.text))
            if self.verif_response(response):
                logging.info('remote access successfully created {}'.format(info["address"]))
                return CBWParser().parse_response(CBWRemoteAccess, response)

        logging.error("Error create connection remote access")
        return False

    def remote_access(self, remote_access_id):
        """GET request to /api/v2/remote_accesses/{remote_access_id} to get all informations
        about a specific remote access"""
        response = self._request("GET", [ROUTE_REMOTE_ACCESSES, remote_access_id])

        if response.status_code != 200:
            logging.error("error remote_access_id::{}".format(response.text))
            return None

        return CBWParser().parse_response(CBWRemoteAccess, response)

    def delete_remote_access(self, remote_access_id):
        """DELETE request to /api/v2/remote_access/{remote_id} to delete a specific remote access"""
        if remote_access_id:
            logging.debug("Deleting remote access {}".format(remote_access_id))
            response = self._request("DELETE", [ROUTE_REMOTE_ACCESSES, remote_access_id])
            return self.verif_response(response)

        logging.error("No remote_access_id for delete")
        return False

    def update_remote_access(self, remote_access_id, info):
        """PATCH request to /api/v2/remote_accesses/{remote_id} to update a remote access"""
        if remote_access_id and info:
            response = self._request("PATCH", [ROUTE_REMOTE_ACCESSES, remote_access_id], info)
            logging.debug("Update remote access::{}".format(response.text))
            return self.verif_response(response)

        logging.error("Error update remote access")
        return False
