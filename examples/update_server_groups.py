"""Update server groups"""

from cbw_api_toolbox.cbw_api import CBWApi

API_KEY = ''
SECRET_KEY = ''
API_URL = ''

CLIENT = CBWApi(API_URL, API_KEY, SECRET_KEY)

SERVER_ID = ''              #add the appropriate id server

INFO = {
    "groups": '',           # The list of the groups names you want to set on your
                            # server split by ',' (ex: 'Production,Developement,etc')

    "compliance_groups": '' # The list of the compliance groups names you want to set on your
                            # server split by ',' (ex: 'Anssi,CIS_Benchmark,etc')
}

CLIENT.update_server(SERVER_ID, INFO)
