"""Update server attributes"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

SERVER_ID = ''                  #add the appropriate id server

INFO = {
    "category": '',
    "description": "",
    "environment": {},          # Environment object
    "deploying_period": "",
    "ignoring_policy": "",
    "compliance_groups": [],    # An array of of the compliance groups IDs you want to set on your
                                # server split by ',' (ex: [13, 20])

    "groups": []                # An array of groups IDs you want to set on your
                                # server split by ',' (ex: [1, 2])

}

CLIENT.update_server(SERVER_ID, INFO)
