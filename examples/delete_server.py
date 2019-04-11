from cbw_api_toolbox.cbw_api import CBWApi

API_KEY = ''
SECRET_KEY = ''
API_URL = ''

CLIENT = CBWApi(API_URL, API_KEY, SECRET_KEY)

CLIENT.ping()

SERVER_ID = '' #Id of the server you which to delete 

result = CLIENT.delete_server(SERVER_ID) 

if result:
    print('Successfull deletion')
else:
    print('Failure deletion')
