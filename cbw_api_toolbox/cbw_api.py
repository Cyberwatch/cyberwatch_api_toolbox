"""Module used to communicate with the CBW API"""

import json
import logging
import sys

import requests
from requests.exceptions import ProxyError, SSLError, RetryError, InvalidHeader, MissingSchema
from urllib3.exceptions import NewConnectionError, MaxRetryError

from cbw_api_toolbox import API_DEFAULT_URL
from cbw_api_toolbox.__routes__ import ROUTE_SERVERS, ROUTE_PING
from cbw_api_toolbox.cbw_auth import CBWAuth
from cbw_api_toolbox.cbw_objects.cbw_server import CBWServer
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

    def ping(self):
        """GET request to /api/v2/ping then check uuid value"""
        response = self._request("GET", [ROUTE_PING])

        if response.status_code == 200:
            print("OK")
            return True

        print("KO")
        return False

    def servers(self):
        """GET request to /api/v2/servers to get all servers"""
        response = self._request("GET", [ROUTE_SERVERS])

        return CBWParser().parse_response(CBWServer, response)

    def server(self, server_id):
        """GET request to /api/v2/servers to get all informations about a specific server"""
        response = self._request("GET", [ROUTE_SERVERS, server_id])

        return CBWParser().parse_response(CBWServer, response)
