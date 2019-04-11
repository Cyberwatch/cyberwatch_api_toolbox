"""CBWAuth module"""

import base64
import datetime
import hmac
from hashlib import sha256

from requests.auth import AuthBase

from cbw_api_toolbox import JSON_CONTENT_TYPE, SIGNATURE_HTTP_HEADER, \
                            TIMESTAMP_HTTP_HEADER, \
                            CONTENT_TYPE_HEADER, SIGNATURE_HEADER


class CBWAuth(AuthBase):
    """Used to make the authentication for the API requests"""

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

        self.raw_data = ""
        self.hash_data = ""
        self.type_data = ""

    def __call__(self, request):
        self._encode(request)
        return request

    def _encode(self, request):
        timestamp = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

        # get data
        self.raw_data = request.body if request.body else ""
        self.type_data = JSON_CONTENT_TYPE if self.raw_data else ""

        # add headers
        if self.raw_data:
            self._add_content_type(request)
        request.headers[TIMESTAMP_HTTP_HEADER] = timestamp
        self._add_signature(request, timestamp)

    def _add_signature(self, request, timestamp):
        method = request.method
        path = request.path_url
        signature = self._sign(method, timestamp, path).decode("utf-8")
        request.headers[SIGNATURE_HTTP_HEADER] = "{0} {1}:{2}".format(SIGNATURE_HEADER,
                                                                      self.api_key,
                                                                      signature)

    def _add_content_type(self, request):
        request.headers[CONTENT_TYPE_HEADER] = self.type_data

    def _sign(self, method, timestamp, path):
        # Build the message to sign
        message = ",".join([method, self.type_data, self.hash_data, path, timestamp])

        # Create the signature
        digest = hmac.new(bytes(self.secret_key, "utf8"), bytes(message, "utf8"), sha256).digest()

        return base64.b64encode(digest).strip()
