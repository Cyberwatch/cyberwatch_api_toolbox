"""Create remote access"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))
INFO = {"type": "", #mandatory, precises the type of the connection
        "address": "", #mandatory, precises the IP address or the domain name of the targeted computer
        "port": "", #mandatory, precises the port of the connection
        "login": "", #precises the login of the connection
        "password": "", #precises the password of the connection
        "key": "", #precises the key of the connection
        "node_id": "", # node_id to link the new agentless connection to
        "server_groups": "", #precise the groups to be added to the computer ("group" or "groupA,groupB,groupC"...)
        "priv_password": "", #for SNMP, encryption password allowing to connect to the computer.
        "auth_password": "" #for SNMP, authentication password allowing to connect to the computer.
        }

CLIENT.create_remote_access(INFO)
