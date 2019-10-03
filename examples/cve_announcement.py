"""GET request to /api/v2/cve_announcements/{CVE_CODE} to get all informations
about a specific cve_announcement"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

CVE_CODE = 'CVE-2017-0146'

CLIENT.cve_announcement(CVE_CODE)
