"""remote access"""

from cbw_api_toolbox.cbw_api import CBWApi

API_KEY = ''
SECRET_KEY = ''
API_URL = ''
REMOTE_ACCESS_ID = ''

CLIENT = CBWApi(API_URL, API_KEY, SECRET_KEY)

CLIENT.remote_access(REMOTE_ACCESS_ID)
