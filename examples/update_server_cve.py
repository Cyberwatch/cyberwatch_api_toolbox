"""Update server cve"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

INFO = {"comment": "", #precises the comment of the cve
        "ignored": "", #boolean, precises if cve is ignored
        }

SERVER_ID = ''

CVE_CODE = ''

CLIENT.update_server_cve(SERVER_ID, CVE_CODE, INFO)
