import json
import logging
from json import JSONDecodeError

import requests
from requests.exceptions import ProxyError, SSLError, RetryError, InvalidHeader, ConnectionError
from urllib3.exceptions import NewConnectionError, MaxRetryError

from cbw_api_toolbox import API_DEFAULT_URL
from cbw_api_toolbox.__routes__ import ROUTE_GET_SERVERS, ROUTE_GET_PING
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

    def _request(self, route, params=None):
        raw_response = None
        try:
            raw_response = requests.get("{0}{1}{2}".format(self.api_url, route, self._get_params(params)),
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

    def ping(self):
        result = self._request(ROUTE_GET_PING)
        print("OK") if result and 'uuid' in result else self.logger.error("FAILED")

    def servers(self):
        return [CBWParser().parse(CBWServer, server) for server in self._request(ROUTE_GET_SERVERS)]

    def server(self, server_id):
        return CBWParser().parse(CBWServer, self._request(ROUTE_GET_SERVERS, [server_id]))

    def get_detailed_servers(self):
        return [self.server(server.server_id) for server in self.servers()]
