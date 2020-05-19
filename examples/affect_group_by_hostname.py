"""Script affecting group(s) depending on hostname of the computers"""

import os
import re
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get(
    'cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

def build_groups_list(server_id, new_groups):
    """Append a list of groups to the list of a computer's existing groups"""
    server_groups = CLIENT.server(str(server_id)).groups
    all_groups = new_groups
    if server_groups:
        for group in server_groups:
            all_groups.append(group.name)
    return all_groups

# Dictionnary of regex corresponding to group(s)
# In this example:
#   - hostname matching the regex "^.*desktop.*$" will be affected the "desktop" group
#   - hostname matching the regex "^.*test.*$" will be affected both "dev_computers" and "test_api_example" groups
HOSTNAME_REGEX = {
        "^.*desktop.*$": "desktop",
        "^.*test.*$": "dev_computers, test_api_example"
}

# Groups are linked to a regex, if a hostname matches the regex it is affected the corresponding group(s)
for server in CLIENT.servers():
    if server.hostname is not None:
        for regex, groups in HOSTNAME_REGEX.items():
            if re.search(regex, server.hostname, flags=re.IGNORECASE):
                groups_list = build_groups_list(server.id, groups.split(','))
                print("hostname : {} - groups : {}".format(server.hostname, groups_list))
                CLIENT.update_server(str(server.id), {'groups': ",".join(groups_list)})
