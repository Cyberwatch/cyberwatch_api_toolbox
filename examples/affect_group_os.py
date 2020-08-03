"""Script affecting a group depending on OS"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get(
    'cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

LINUX_OS = ['Amazon', 'ArchLinux', 'Centos', 'Debian', 'Manjaro', 'Oracle', 'Ubuntu', 'Redhat', 'Suse']
WINDOWS_OS = ['Windows']
MAC_OS = ['Macos']

LINUX_GROUP_ID = ''
MAC_GROUP_ID = ''
WINDOWS_GROUP_ID = ''
OTHER_GROUP_ID = ''


def build_groups_list(server_id, system_os):
    """Create list with system_os + other groups of server"""
    server = CLIENT.server(str(server_id))
    server_groups = [system_os]
    if server.groups:
        for group in server.groups:
            server_groups.append(group.name)
    return server_groups

for server_item in CLIENT.servers():
    if server_item.os is not None:
        if server_item.os.type[4:] in LINUX_OS:
            GROUP_ID = LINUX_GROUP_ID
        elif server_item.os.type[4:] in WINDOWS_OS:
            GROUP_ID = WINDOWS_GROUP_ID
        elif server_item.os.type[4:] in MAC_OS:
            GROUP_ID = MAC_GROUP_ID
        else:
            GROUP_ID = OTHER_GROUP_ID

    CLIENT.update_server(str(server_item.id), {'groups': [GROUP_ID]})
