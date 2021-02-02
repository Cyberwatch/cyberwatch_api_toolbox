"""Create applicative scan for network target or website"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

INFO = {
    "target": "",  # Mandatory address of the network target or the website..
    "node_id": "", # Mandatory node that will perform the scans to the network target or website.
}

CLIENT.create_applicative_scan(INFO)
