"""import file xlsx"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_file_xlsx import CBWXlsx

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
XLSX = CBWXlsx(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

FILE_XLSX = 'import_file.xlsx'

RESPONSE = XLSX.import_remote_accesses_xlsx(FILE_XLSX)

if RESPONSE:
    for remote_access in RESPONSE:
        if remote_access:
            print("remote access created, id=>>>>>{}".format(remote_access.id))
        else:
            print("An error occurred, import_remote_accesses_xlsx failed")
else:
    print("Error format file xlsx::HOST, PORT, TYPE, USERNAME, PASSWORD, KEY, NODE, SERVER_GROUPS")
