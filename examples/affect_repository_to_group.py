"""
Script affecting a custom repository to servers in a specific group
Prerequisite :
- Set the constant variables on the first lines of the script
"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

GROUP_NAME = ''

# Find the REPOSITORY_ID on [CYBERWATCH_URL]/compliance/groups/customs and edit
# the concerned custom repository (the ID will be in the URL)
# Example: "https://[CYBERWATCH_URL]/compliance/groups/customs/13/edit" the REPOSITORY_ID is '13'
REPOSITORY_ID = ''

def connect_api():
    '''Connect to the API and test connection'''
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '..', 'api.conf'))
    client = CBWApi(conf.get('cyberwatch', 'url'), conf.get(
        'cyberwatch', 'api_key'), conf.get('cyberwatch', 'secret_key'))

    client.ping()
    return client

def affect_repository_to_servers(group_name, repository_id, client):
    '''Build server list with a specific group and affect them a custom repository'''
    servers = client.servers()
    for server in servers:
        for group in server.groups:
            if group.name == group_name:
                client.update_compliance_server(str(server.id), {"compliance_groups": [str(repository_id)]})

def launch_script():
    '''Launch script'''
    client = connect_api()
    if GROUP_NAME and REPOSITORY_ID:
        if REPOSITORY_ID.isdigit():
            print("INFO: Using `{}` for group name and {} for repository ID.".format(GROUP_NAME, REPOSITORY_ID))
            affect_repository_to_servers(GROUP_NAME, REPOSITORY_ID, client)
            print("INFO: Done.")
        else:
            print("ERROR: REPOSITORY_ID is not valid integer, exiting...")
    else:
        print("ERROR: GROUP_NAME or REPOSITORY_ID variable not provided, exiting...")


launch_script()
