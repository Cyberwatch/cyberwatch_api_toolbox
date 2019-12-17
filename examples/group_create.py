"""POST request to /api/v3/groups to create a new group"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

PARAMS = {
    "name": "", #Required, name of the group
    "description": "", #Description of the created group
    "color": "" #Colour of the group
}

CLIENT.create_group(PARAMS)
