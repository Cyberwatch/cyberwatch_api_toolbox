"""Example: Find agents by last communication time"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

CLIENT.ping()

AGENTS = CLIENT.agents()

LAST_COMMUNICATION_BEFORE = '2019-09-26'
SELECTED_AGENTS = []

for agent in AGENTS:
    if agent.last_communication < LAST_COMMUNICATION_BEFORE:
        SELECTED_AGENTS.append(agent)
