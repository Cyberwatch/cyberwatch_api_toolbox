"""Create security issue"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

INFO = {
    "sid": "",  # Mandatory SID of the security issue
    "cve_announcements": [], # List of cve_announcements Code related to the security issue.
    "description": "",  # Description of the security issue
    "level": "",  # Severity of the security issue
    "score": "",  # Score of the security issue
    "servers": [],  # ID list of servers affected by the security issue.
    "title": ""  # Title of the security issue
}

CLIENT.create_security_issue(INFO)
