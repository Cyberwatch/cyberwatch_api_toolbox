"""Update a stored credentials"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

INFO = {"type": "", #precises the type of the stored credentials
        "name": "", #precises the name of the stored credentials
        "endpoint": "", #entry point (URL) for credentials of type docker engine or docker registry.
        "user": "", #precises the user of the stored credentials
        "password": "", #precises the password in the stored credentials
        "key": "", #precises the secret key for credentials of type key
        "ca_cert": "", #certificate of the certificate authority for TLS credentials like a docker engine.
        "client_cert": "", #precise client private key for TLS credentials like a Docker engine.
        "client_key": "", #client certificate for TLS credentials like a Docker engine.
        "auth_password": "", #for SNMP, authentication password for SNMP credentials.
        "priv_password": "" #for SNMP, encryption password for SNMP credentials.
        }

STORED_CREDENTIALS_ID = ''

CLIENT.update_stored_credential(STORED_CREDENTIALS_ID, INFO)
