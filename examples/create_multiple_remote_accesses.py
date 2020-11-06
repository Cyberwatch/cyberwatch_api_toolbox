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


def get_addresses(client):
    '''Get all addresses of remote accesses in Cyberwatch'''
    remote_accesses_ip = []
    for remote_access in client.remote_accesses():
        remote_accesses_ip.append(
            {"server_id": remote_access.server_id, "address": remote_access.address})
    return remote_accesses_ip


def verify_exist(value, existing_list, key):
    """Verify if value exist in a list of dict and return the index"""
    for i, dic in enumerate(existing_list):
        if dic[key] == value:
            return i
    return None


def create_groups(groups, client):
    """Find all groups and create new groups if needed"""
    to_add = []
    existing_groups = []

    for pair in groups:
        pair_groups = list(pair.values())
        for group in pair_groups:
            for cleaned_group in group.split(","):
                to_add.append(cleaned_group.strip())

    for existing_group in client.groups():
        existing_groups.append(
            {"id": existing_group.id, "group_name": existing_group.name})

    for group_name in to_add:
        if not any(d['group_name'] == group_name for d in existing_groups):
            created_group = client.create_group({"name": group_name})
            existing_groups.append(
                {"id": created_group.id, "group_name": created_group.name})

    return existing_groups


def get_groups_id(server_id, all_groups, new_groups, client):
    """Build list of group ID for the asset"""
    groups_id = []

    server_details = client.server(str(server_id))
    for group in server_details.groups:
        groups_id.append(group.id)

    cleaned_groups_name = []
    for group in new_groups:
        for name in group.split(","):
            cleaned_groups_name.append(name.strip())

    for group_name in cleaned_groups_name:
        group_id = all_groups[verify_exist(
            group_name, all_groups, "group_name")]
        groups_id.append(group_id["id"])

    return groups_id


def create_servers(addresses, credential_id, existing_addresses, groups, client):
    '''Create agentless connection or update existing one'''
    for pair in addresses:
        pair_address = list(pair.keys())
        pair_groups = list(pair.values())

        index = verify_exist(pair_address[0], existing_addresses, "address")
        if index is not None:
            if existing_addresses[index]["server_id"] is not None:
                groups_id = get_groups_id(
                    existing_addresses[index]["server_id"], groups, pair_groups, client)
                params = {
                    "groups": groups_id
                }
                client.update_server(str(existing_addresses[index]["server_id"]), params)
            else:
                print("ERROR: Remote access '{}' has no server ID".format(pair_address[0]))
        else:
            params = {
                "type": "CbwRam::RemoteAccess::Ssh::WithKey",
                "address": pair_address[0],
                "port": "22",
                "credential_id": credential_id,
                "node_id": "1",
                "server_groups": pair_groups[0]
            }

            client.create_remote_access(params)

def launch_script():
    '''Launch script'''
    client = connect_api()
    current_addresses = get_addresses(client)
    groups = create_groups(ADDRESSES, client)
    create_servers(ADDRESSES, CREDENTIAL_ID, current_addresses, groups, client)


launch_script()
