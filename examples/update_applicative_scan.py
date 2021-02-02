"""Update applicative scan for network target or website"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

APPLICATIVE_SCAN_ID = '' # ID of the applicative scan.

INFO = {
    "target": "",  # Optional address of the network target or the website to update.
    "node_id": "", # Optional node that will perform the scans to the network target or website to update.
}

CLIENT.update_applicative_scan(APPLICATIVE_SCAN_ID, INFO)
