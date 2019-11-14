"""Make the directory as a package directory"""

import logging
import urllib3

urllib3.disable_warnings()

logging.basicConfig(level=logging.INFO)


SIGNATURE_HEADER = 'CyberWatch APIAuth-HMAC-SHA256'
SIGNATURE_HTTP_HEADER = 'Authorization'
TIMESTAMP_HTTP_HEADER = 'Date'
SIGNATURE_DELIM = ':'
CONTENT_TYPE_HEADER = 'Content-Type'
JSON_CONTENT_TYPE = 'application/json'
