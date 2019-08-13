# -*- coding: utf-8 -*-

"""
Example of sending data to Splunk.
Documentation related to the script is available in Cyberwatch: https://[CYBERWATCH_URL]/help/en/5_connect_cyberwatch_third_party/import_data_siem.md
"""

import requests
import os
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
conf = ConfigParser()
conf.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))

# Retrieve the computer from Cyberwatch API
CLIENT = CBWApi(conf.get('cyberwatch', 'url'), conf.get('cyberwatch', 'api_key'), conf.get('cyberwatch', 'secret_key'))
SERVER_ID = ''
server = CLIENT.server(SERVER_ID)

# Send the data to Splunk
post_splunk(conf.get('splunk', 'url'), conf.get('splunk', 'token'), '- Hostname: {}\n- Vulnerabilities count: {}'.format(server.hostname, server.cve_announcements_count))
