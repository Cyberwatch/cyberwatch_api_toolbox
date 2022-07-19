"""
Please provide the path to the CSV file in your api.conf file using this format:
[file]
csv_file = PATH/TO/FILE
"""

import csv
import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi
# pylint: disable=W0621

def connect_api():
    '''Connect to the API and test connection'''
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '..', 'api.conf'))
    client = CBWApi(conf.get('cyberwatch', 'api_url'), conf.get(
        'cyberwatch', 'api_key'), conf.get('cyberwatch', 'secret_key'))

    client.ping()
    return client

def get_file_name():
    '''Get the name of the CSV file'''
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '..', 'api.conf'))
    file = conf.get('file', 'csv_file')

    return file

def get_groups_by_name_id(client):
    """get_groups_by_name_id"""
    groups_by_name_id = {}
    for group in client.groups():
        groups_by_name_id[group.name] = group.id
    return groups_by_name_id

def get_assets_by_hostname_id(client):
    """get_assets_by_hostname_id"""
    assets_by_hostname_id = {}
    for asset in client.assets():
        assets_by_hostname_id[asset.hostname] = asset.id
    return assets_by_hostname_id

def get_asset_groups_by_id(client, asset_id):
    """get_asset_groups_by_asset_id"""
    groups = []
    for group in client.asset(asset_id).groups:
        groups.append(group.asset_id)
    return groups

# Connect to Cyberwatch API
CLIENT = connect_api()

# Read the CSV file and extract elements
FILE = open(get_file_name(), encoding="utf-8") # pylint: disable=R1732
CSVREADER = csv.reader(FILE)
next(CSVREADER) #comment this line if the CSV file doesn't have headers

# Associate each asset in Cyberwatch to its ID
HOSTNAME_ID = get_assets_by_hostname_id(CLIENT)

# Associate each group in Cyberwatch to its ID
GROUP_ID = get_groups_by_name_id(CLIENT)

for element in CSVREADER:
    #Separate hostname and groups from the extracted data
    elements = str(element[0]).split(";")

    #Get hostname and ID
    hostname = elements[0]
    ID = HOSTNAME_ID[hostname]

    #Get groups that are already associated to the asset
    total_groups = get_asset_groups_by_id(CLIENT, str(ID))

    # Append new groups to the total
    groups = str(elements[1]).split(":")
    for group in groups:
        total_groups.append(GROUP_ID[group])

    # Update asset information in Cyberwatch
    PARAMS = {
        "groups": total_groups
    }
    CLIENT.update_server(str(ID), PARAMS)
