"""Export remote accesses in file xlsx"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_file_xlsx import CBWXlsx

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
XLSX = CBWXlsx(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

FILE_XLSX = "" #Optional parameter

print(XLSX.export_remote_accesses_xlsx())
