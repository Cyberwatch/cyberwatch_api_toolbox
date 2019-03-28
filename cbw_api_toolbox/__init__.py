"""Make the directory as a package directory"""

import urllib3
urllib3.disable_warnings()

API_DEFAULT_URL = "/api/v2/"

SIGNATURE_HEADER = 'CyberWatch APIAuth-HMAC-SHA256'
SIGNATURE_HTTP_HEADER = 'Authorization'
TIMESTAMP_HTTP_HEADER = 'Date'
SIGNATURE_DELIM = ':'
CONTENT_HASH_HEADER = 'Content-MD5'
CONTENT_TYPE_HEADER = 'Content-Type'
JSON_CONTENT_TYPE = 'application/json'
