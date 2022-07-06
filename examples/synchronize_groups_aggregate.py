"""
Script for synchronizing group(s) between local and aggregate node (for aggregation mode)

Please provide the nodes information in your api.conf file using this format:
[local_node]
api_key = ...
secret_key = ...
url = https://myinstance.local

[aggregation_node]
api_key = ...
secret_key = ...
url = https://myinstance.aggregate
"""

import os
from configparser import ConfigParser
from urllib.parse import parse_qs

from requests.api import get
from cbw_api_toolbox.cbw_api import CBWApi

def connect_api(node):
    '''Connect to the API and test connection'''
    CONF = ConfigParser()
    CONF.read(os.path.join(os.path.abspath(
    os.path.dirname(__file__)), '.', 'api.conf'))
    client = CBWApi(CONF.get(node, 'url'), CONF.get(
        node, 'api_key'), CONF.get(node, 'secret_key'))
    client.ping()
    return client

def get_groups(client):
    '''get all groups of an instance by their names'''
    groups_by_name = []
    for group in client.groups():
        groups_by_name.append(group.name)
    return groups_by_name

def create_groups_on_aggregation_node(groups, client):
    '''create the missing groups on the aggregation node'''
    for group in groups:
        PARAMETERS = {"name": group, "description": "Group from aggregation", "color": "#fa824c"}
        client.create_group(PARAMETERS)

def get_assets_by_hostname_id(client):
    '''get all assets of an instance by their hostnames and ids'''
    assets_by_hostname_id = {}
    for asset in client.assets():
        assets_by_hostname_id[asset.hostname] = asset.id
    return assets_by_hostname_id

def get_asset_groups(node_assets):
    '''get assiociated groups of an asset'''
    dict_asset_groups = {}
    for node_asset in node_assets:
        groups = []
        if node_asset.groups:
            for group in node_asset.groups:
                groups.append(group.name)
            dict_asset_groups[node_asset.hostname] = groups
    return dict_asset_groups

#------------------------
# Create the missing groups on aggregate node
#------------------------

# Connection to both instances
client_local = connect_api('local_node')
client_aggregate = connect_api('aggregation_node')

# Get local and aggregate groups
groups_local = get_groups(client_local)
groups_aggregate = get_groups(client_aggregate)

# Get groups to create
groups_in_common = set(groups_local) & set(groups_aggregate)
print(groups_in_common)
groups_present_only_locally = set(groups_local) - groups_in_common
print(groups_present_only_locally)

# Create the missing groupes
create_groups_on_aggregation_node(groups_present_only_locally, client_aggregate)

#------------------------
# Add missing groups to assets on aggregation node
#------------------------

# Get all assets on both instances
local_assets = client_local.assets()
aggregate_assets = client_aggregate.assets()

# Hostname - ID association
local_assets_by_hostname_id = get_assets_by_hostname_id(client_local)
aggregate_assets_by_hostname_id = get_assets_by_hostname_id(client_aggregate)

# asset:groups - local 
dict_asset_groups_local = get_asset_groups(local_assets)

# asset:groupes - aggregate (filtered on locally present assets)
dict_asset_groups_aggregate = {}

for aggregate_asset in aggregate_assets:
    if aggregate_asset.hostname in dict_asset_groups_local.keys():
        groups = []
        if aggregate_asset.groups:
            for group in aggregate_asset.groups:
                groups.append(group.name)
            dict_asset_groups_aggregate[aggregate_asset.hostname] = groups

# groups : name - ID
aggregate_groups = {}
for group in client_aggregate.groups():
    aggregate_groups[group.name] = group.id

# Add missing groups to assets on aggregation node - assets with groups on aggregate case
if dict_asset_groups_aggregate:
    for asset in dict_asset_groups_local:
        if asset in dict_asset_groups_aggregate:
            groups_in_common = set(dict_asset_groups_local[asset]) & set(dict_asset_groups_aggregate[asset])
            groups_only_local = set(dict_asset_groups_local[asset]) - groups_in_common
            groups_in_total = set(dict_asset_groups_aggregate[asset]) | set(groups_only_local)

            groups_to_add = []
            for group in groups_in_total:
                groups_to_add.append(aggregate_groups[group])
            PARAMS = { "groups": groups_to_add}
            client_aggregate.update_server(str(aggregate_assets_by_hostname_id[asset]),PARAMS)
        else:
            groups_to_add = []
            for group in dict_asset_groups_local[asset]:
                groups_to_add.append(aggregate_groups[group])
            PARAMS = { "groups": groups_to_add}
            client_aggregate.update_server(str(aggregate_assets_by_hostname_id[asset]),PARAMS)
            
# Add missing groups to assets on aggregation node - assets without groups without groups case
else:
    for asset in dict_asset_groups_local:
        groups_to_add = []
        for group in dict_asset_groups_local[asset]:
            groups_to_add.append(aggregate_groups[group])
        PARAMS = { "groups": groups_to_add}
        client_aggregate.update_server(str(aggregate_assets_by_hostname_id[asset]),PARAMS)
