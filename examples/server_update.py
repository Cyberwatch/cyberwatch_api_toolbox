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
    "criticality": '',          #(ex: 'criticality_low, criticality_medium, etc')
    "deploying_period": "",
    "ignoring_policy": "",
    "compliance_groups": '',    # The list of the compliance groups names you want to set on your
                                # server split by ',' (ex: 'Anssi, CIS_Benchmark, etc')

    "groups": ''                # The list of the groups names you want to set on your
                                # server split by ',' (ex: 'Production, Developement, etc')

}

CLIENT.update_server(SERVER_ID, INFO)
