"""
Please provide the path to the CSV file in your api.conf file using this format:
[file]
csv_file = PATH/TO/FILE
"""

import argparse
from argparse import RawTextHelpFormatter
import os
import json
from configparser import ConfigParser
import requests
from cbw_api_toolbox.cbw_api import CBWApi
from requests.auth import HTTPBasicAuth
import csv

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
    groups_by_name_id = {}
    for group in client.groups():
        groups_by_name_id[group.name] = group.id
    return groups_by_name_id

def get_assets_by_hostname_id(client):
    assets_by_hostname_id = {}
    for asset in client.assets():
        assets_by_hostname_id[asset.hostname] = asset.id
    return assets_by_hostname_id

def get_asset_groups_by_id(client, id):
    groups = []
    for group in client.asset(id).groups:
        groups.append(group.id)
    return groups

# Connect to Cyberwatch API
client = connect_api()

# Read the CSV file and extract elements
file = open(get_file_name())
csvreader = csv.reader(file)
next(csvreader) #comment this line if the CSV file doesn't have headers

# Associate each asset in Cyberwatch to its ID
hostname_id = get_assets_by_hostname_id(client)

# Associate each group in Cyberwatch to its ID
group_id = get_groups_by_name_id(client)

for element in csvreader:
    #Separate hostname and groups from the extracted data
    elements = str(element[0]).split(";")

    #Get hostname and ID
    hostname = elements[0]
    ID = hostname_id[hostname]

    #Get groups that are already associated to the asset
    total_groups = get_asset_groups_by_id(client, str(ID))

    # Append new groups to the total 
    groups = str(elements[1]).split(":")
    for group in groups:
        total_groups.append(group_id[group])

    # Update asset information in Cyberwatch
    PARAMS = {
        "groups": total_groups
    }
    client.update_server(str(ID), PARAMS)
