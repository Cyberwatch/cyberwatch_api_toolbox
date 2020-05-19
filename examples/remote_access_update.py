"""Update remote access"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

INFO = {"address": "", #mandatory, precises the IP address or the domain name of the targeted computer
        "node_id": "", #precises the Cyberwatch source of the connection
        "priv_password": "", #for SNMP, encryption password allowing to connect to the computer.
        "auth_password": "", #for SNMP, authentication password allowing to connect to the computer.
        "port": "", #mandatory, precises the port of the connection
        "login": "", #precises the login of the connection
        "password": "", #precises the password of the connection
        "key": "", #precises the key of the connection
        }

REMOTE_ACCESS_ID = ''

CLIENT.update_remote_access(REMOTE_ACCESS_ID, INFO)
