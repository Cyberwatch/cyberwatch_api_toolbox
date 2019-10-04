'''Delete a Server'''

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

CLIENT.ping()

SERVER_ID = '' #Id of the server you which to delete

RESULT = CLIENT.delete_server(SERVER_ID)

if RESULT:
    print('Successfull deletion')
else:
    print('Failure deletion')
