# -*- coding: utf-8 -*-

"""
Example script to affect groups to computers depending on their operating system.
Every computer based on Windows system will be added to "WINDOWS" group and Unix systems to "UNIX".
"""

import requests
import os
import sys
from six.moves.configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

# Load configuration from file api.conf
conf = ConfigParser()
conf.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))

# Retrieve the computer from Cyberwatch API
CLIENT = CBWApi(conf.get('cyberwatch', 'url'), conf.get('cyberwatch', 'api_key'), conf.get('cyberwatch', 'secret_key'))

servers = CLIENT.servers()

unix_os = ['Amazon', 'ArchLinux', 'Centos', 'Debian', 'Manjaro', 'Oracle', 'Ubuntu', 'Redhat', 'Suse']
windows_os = ['Windows']
mac_os = ['Macos']

print(len(servers))

# ON HOLD : Necessite d'avoir la route /groups ajoutée dans l'API. Pour récupérer l'id des groups dans lesquels on veut ajouter les machines
for server in servers:
    server = CLIENT.server(server.id)
    if not (server.os is None):
        if server.os["type"][4:] in unix_os:
            if not (server.groups is None):
                server.groups.append(
        if server.os["type"][4:] in windows_os:
            pass
        if server.os["type"][4:] in mac_os:
            pass
