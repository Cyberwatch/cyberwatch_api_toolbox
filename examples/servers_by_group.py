"""Example: Find all servers per group"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

CLIENT.ping()

SERVERS = CLIENT.servers()

CATEGORY_BY_GROUPS = {}

# append each server to a group by category dict
for server in SERVERS:
    server = CLIENT.server(str(server.id))

    for group in server.groups:
        if group.name not in CATEGORY_BY_GROUPS:
            CATEGORY_BY_GROUPS[group.name] = {}

        concerned_group = CATEGORY_BY_GROUPS[group.name]

        if server.category not in concerned_group:
            concerned_group[server.category] = []

        concerned_group[server.category].append(server)

for group in CATEGORY_BY_GROUPS.items():
    print("--- GROUP : {0} ---".format(group))

    for category in CATEGORY_BY_GROUPS[group]:
        print("{0}  : {1}".format(category, len(CATEGORY_BY_GROUPS[group][category])))

        for server in CATEGORY_BY_GROUPS[group][category]:
            print("{0} with hostname : {1}".format(category, server.hostname))
