"""
Example of sending data to Splunk.
Documentation related to the script is available in Cyberwatch:
https://[CYBERWATCH_URL]/help/en/5_connect_cyberwatch_third_party/import_data_siem.md
"""

import os
import requests
from six.moves.configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

def post_splunk(url, token, payload):
    """
        Send a post request to Splunk API
    """
    headers = {'Authorization': 'Splunk {}'.format(token)}
    res = requests.post(url=url, headers=headers, data=payload, verify=False)
    res.raise_for_status()
    return res.json()

# Load configuration from file api.conf
CONF = ConfigParser()


CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))

# Retrieve the computer from Cyberwatch API
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))
SERVER_ID = ''
SERVER = CLIENT.server(SERVER_ID)

# Send the data to Splunk
post_splunk(CONF.get('splunk', 'url'), CONF.get('splunk', 'token'),
            '- Hostname: {}\n- Vulnerabilities count: {}'.format(SERVER.hostname, SERVER.cve_announcements_count))
