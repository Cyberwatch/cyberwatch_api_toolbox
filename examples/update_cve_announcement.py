"""Update cve_announcement"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(
    os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get(
    'cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

INFO = {"score_custom": "",
        "access_complexity": "",
        "access_vector": "",
        "availability_impact": "",
        "confidentiality_impact": "",
        "integrity_impact": "",
        "privilege_required": "",
        "scope": "",
        "user_interaction": ""
        }

CVE_CODE = ''

CLIENT.update_cve_announcement(CVE_CODE, INFO)
