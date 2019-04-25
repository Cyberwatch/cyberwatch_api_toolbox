"""Update server groups"""

from cbw_api_toolbox.cbw_api import CBWApi

API_KEY = ''
SECRET_KEY = ''
API_URL = ''

CLIENT = CBWApi(API_URL, API_KEY, SECRET_KEY)

SERVER_ID = ''                  #add the appropriate id server

INFO = {
    "category": '',
    "description": "",
    "criticality": '',          #(ex: 'criticality_low, criticality_medium, etc')
    "deploying_period": "",
    "ignoring_policy": "",
    "compliance_groups": '',    # The list of the compliance groups names you want to set on your
                                # server split by ',' (ex: 'Anssi, CIS_Benchmark, etc')

    "groups": ''                # The list of the groups names you want to set on your
                                # server split by ',' (ex: 'Production, Developement, etc')

}

CLIENT.update_server(SERVER_ID, INFO)
