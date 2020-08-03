"""View the server updates"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

SERVER_ID = ""  # add the server id

SERVER = CLIENT.server(str(SERVER_ID))

print("Server : {}".format(SERVER.hostname))
print("Update count : {}".format(SERVER.updates_count))

print("Updates :")
for update in SERVER.updates:
    print("\t-Product : {}".format(update.current.product))
    print("\t\t- Corrective action : {0} -> {1}".format(update.current.version,
                                                        update.target.version))

    cve_list = []
    for cve in update.cve_announcements:
        cve_list.append(cve)

    print("\t\t- Cve List : {}".format(", ".join(cve_list)))
