"""
Script to create multiple agentless connection with a credential ID and groups
Prerequisite :
- Set the constant variables on the first lines of the script
"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

# Find the ID on [CYBERWATCH_URL]/ram/credentials and edit the concerned stored credential (the ID will be in the URL)
# Example: "https://[CYBERWATCH_URL]/ram/credentials/9/edit" the CREDENTIAL_ID is '9'
CREDENTIAL_ID = ''

ADDRESSES = [] # List of pair of address/groups ([{"adress1": "groupA, groupB"},{"adress2": "groupC"}]...)

def connect_api():
    '''Connect to the API and test connection'''
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '..', 'api.conf'))
    client = CBWApi(conf.get('cyberwatch', 'url'), conf.get(
        'cyberwatch', 'api_key'), conf.get('cyberwatch', 'secret_key'))

    client.ping()
    return client

def create_servers(addresses, credential_id, client):
    '''Create agentless connection with credential id and groups'''
    for pair in addresses:
        address = list(pair.keys())
        groups = list(pair.values())

        params = {
        "type": "CbwRam::RemoteAccess::Ssh::WithKey",
        "address": address[0],
        "port": "22",
        "credential_id": credential_id,
        "node_id": "1",
        "server_groups": groups[0]
        }

        client.create_remote_access(params)

def launch_script():
    '''Launch script'''
    client = connect_api()
    create_servers(ADDRESSES, CREDENTIAL_ID, client)

launch_script()
