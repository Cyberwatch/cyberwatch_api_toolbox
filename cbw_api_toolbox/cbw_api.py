import json
import logging
import os
from json import JSONDecodeError

import requests
from requests.exceptions import ProxyError, SSLError, RetryError, InvalidHeader, ConnectionError, MissingSchema
from urllib3.exceptions import NewConnectionError, MaxRetryError

from cbw_api_toolbox import API_DEFAULT_URL
from cbw_api_toolbox.__routes__ import ROUTE_SERVERS, ROUTE_PING
from cbw_api_toolbox.cbw_auth import CBWAuth
from cbw_api_toolbox.cbw_objects.cbw_server import CBWServer
from cbw_api_toolbox.cbw_parser import CBWParser


class CBWApi(object):
    def __init__(self, api_url, api_key, secret_key, verify_ssl=False):
        self.api_url = api_url + API_DEFAULT_URL
        self.api_key = api_key
        self.secret_key = secret_key

        self.verify_ssl = verify_ssl
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def _get_params(params=None):
        return "/{0}".format('/'.join(params)) if params else ""

    def _request(self, route, verb, params=None):
        raw_response = None
        
        try:
            raw_response = requests.request(
                verb,
                "{0}{1}{2}".format(self.api_url, route, self._get_params(params)),
                data=params,
                auth=CBWAuth(self.api_key, self.secret_key),
                verify=self.verify_ssl)
            return json.loads(raw_response.text)
        except JSONDecodeError as e:
            self.logger.error("An error occurred when decoding {0} with route {1}/{2}{3} : {4}"
                              .format(raw_response.text, self.api_url, route, self._get_params(params), e))
        except (ConnectionError, ProxyError, SSLError, NewConnectionError, RetryError,
                InvalidHeader, MaxRetryError) as e:
            self.logger.error("An error occurred when requesting {0}/{1}{2} : {3}"
                              .format(self.api_url, route, self._get_params(params), e))
        except MissingSchema as e:
            self.logger.error("An error occurred, please check your API_URL.")
            os._exit(-1)

    # GET request to /api/v2/ping then check uuid value
    def ping(self):
        result = self._request(ROUTE_PING, "GET")
        print("OK") if result and 'uuid' in result else self.logger.error("FAILED")

    # GET request to /api/v2/servers to get all servers
    def servers(self):
        return [CBWParser().parse(CBWServer, server) for server in self._request(ROUTE_SERVERS, "GET")]

    # GET request to /api/v2/servers to get all informations about a specific server
    def server(self, server_id):
        return CBWParser().parse(CBWServer, self._request(ROUTE_SERVERS, "GET", [server_id]))

    # Use servers method to get all informations for each server
    def get_detailed_servers(self):
        return [self.server(server.server_id) for server in self.servers()]
