"""Add an ignoring policy to all servers"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

# Find the ID on [CYBERWATCH_URL]/vm/ignoring_policies and edit the concerned policy (the ID will be in the URL)
# Example: "https://[CYBERWATCH_URL]/vm/ignoring_policies/6/edit" will be "ignoring_policy": "6"

INFO = {
    "ignoring_policy": ""
}

for server_item in CLIENT.servers():
    CLIENT.update_server(str(server_item.id), INFO)
