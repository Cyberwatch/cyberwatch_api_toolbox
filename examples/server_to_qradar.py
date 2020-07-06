"""
Example of sending data to qradar.
Documentation related to the script is available in Cyberwatch:
https://[CYBERWATCH_URL]/help/en/5_connect_cyberwatch_third_party/import_data_siem.md
"""

import os
import json
from configparser import ConfigParser
import requests
from cbw_api_toolbox.cbw_api import CBWApi

def post_qradar(url, data_json):
    """
        Send a post request to qradar HTTP Receiver
    """

    headers = {'Content-Type': 'application/json'}
    res = requests.post(url=url, headers=headers, data=data_json, verify=False)
    res.raise_for_status()
    return res.status_code

# Load configuration from file api.conf
CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

# Retrieve the computer from Cyberwatch API
SERVER_ID = ''
SERVER = CLIENT.server(SERVER_ID)

# Example payload to send to qradar

payload = {
    "EventCategory": "Cyberwatch Integration",
    "Hostname": SERVER.hostname,
    "Vulnerabilities count": SERVER.cve_announcements_count,
}

payload_json = json.dumps(payload)

# Send the data to qradar
post_qradar(CONF.get('qradar', 'url'), payload)
