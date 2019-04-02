# delete_server.py
from cbw_api_toolbox.cbw_api import CBWApi

API_KEY = ''
SECRET_KEY = ''
API_URL = ''

SERVER_ID = '' # For this example, you need to specify a server id in addition to your credentials

result = CBWApi(API_URL, API_KEY, SECRET_KEY).delete_server(SERVER_ID)

if result:
    print('Successfull deletion')
else:
    print('Failure')
