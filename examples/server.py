"""get server by server_id"""

from cbw_api_toolbox.cbw_api import CBWApi

API_KEY = ''
SECRET_KEY = ''
API_URL = ''

CLIENT = CBWApi(API_URL, API_KEY, SECRET_KEY)

SERVER_ID = ''

CLIENT.server(SERVER_ID)
