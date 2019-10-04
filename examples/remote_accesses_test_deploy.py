"""Example: Get all invalid remote access and test them"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

for remote_access_item in CLIENT.remote_accesses():
    if remote_access_item.is_valid is False:
        CLIENT.test_deploy_remote_access(str(remote_access_item.id))
