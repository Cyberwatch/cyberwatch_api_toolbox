"""POST request to /api/v3/hosts to create a new host"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

PARAMS = {
    "target": "", #Required, IP address of the new host targeted.
    "node_id": "", #Required, Node ID to link the new Host to.
    "server_id": "", #ID of the server to link the new Host to.
    "hostname": "", #Hostname of the new Host.
    "category": "" #Category of the new Host.
}

CLIENT.create_host(PARAMS)
