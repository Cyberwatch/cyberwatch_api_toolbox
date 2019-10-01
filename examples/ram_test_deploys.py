"""Example: Get all invalid remote access and test them"""

from cbw_api_toolbox.cbw_api import CBWApi

API_KEY = ''
SECRET_KEY = ''
API_URL = ''

CLIENT = CBWApi(API_URL, API_KEY, SECRET_KEY)

for remote_access_item in CLIENT.remote_accesses():
    if remote_access_item.is_valid is False:
        CLIENT.test_deploy_remote_access(str(remote_access_item.id))
