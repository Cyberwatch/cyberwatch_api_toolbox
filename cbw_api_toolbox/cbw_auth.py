import base64
import datetime
import hmac
from hashlib import sha256, md5

from requests.auth import AuthBase

from cbw_api_toolbox import JSON_CONTENT_TYPE, SIGNATURE_HTTP_HEADER, TIMESTAMP_HTTP_HEADER, CONTENT_HASH_HEADER, \
    CONTENT_TYPE_HEADER, SIGNATURE_HEADER


class CBWAuth(AuthBase):
    def __init__(self, api_key: str, secret_key: str):
        self.api_key: str = api_key
        self.secret_key: str = secret_key

        self.raw_data: str = ""
        self.hash_data: str = ""
        self.type_data: str = ""

    def __call__(self, request):
        self._encode(request)
        return request

    def _encode(self, request):
        timestamp = self._get_current_timestamp()

        # get data
        self.raw_data = request.body if request.body else ""
        self.type_data = JSON_CONTENT_TYPE if self.raw_data else ""
        if self.raw_data:
            self._hash_data()

        # add headers
        if self.raw_data:
            self._add_content_type(request)
        self._add_timestamp(request, timestamp)
        self._add_signature(request, timestamp)

    def _hash_data(self):
        self.hash_data = md5(self.raw_data.encode('utf-8')).hexdigest()

    def _get_current_timestamp(self) -> str:
        return datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    def _add_timestamp(self, request, timestamp):
        request.headers[TIMESTAMP_HTTP_HEADER] = timestamp

    def _add_signature(self, request, timestamp):
        method = request.method
        path = request.path_url
        signature = self._sign(method, timestamp, path).decode("utf-8")
        request.headers[SIGNATURE_HTTP_HEADER] = f"{SIGNATURE_HEADER} {self.api_key}:{signature}"

    def _add_content_type(self, request):
        request.headers[CONTENT_HASH_HEADER] = self.hash_data
        request.headers[CONTENT_TYPE_HEADER] = self.type_data

    def _sign(self, method: str, timestamp, path: str):
        # Build the message to sign
        message: str = ",".join([method, self.type_data, self.hash_data, path, timestamp])

        # Create the signature
        digest: bytes = hmac.new(bytes(self.secret_key, "utf8"), bytes(message, "utf8"), sha256).digest()

        return base64.b64encode(digest).strip()
