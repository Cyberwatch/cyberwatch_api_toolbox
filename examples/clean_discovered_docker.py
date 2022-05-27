"""Script used to clean docker images older than X days and not discovered"""

import os
from datetime import datetime
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

# Change to True to delete servers
DELETE = False
# Delete if creation date older than X days
DELETE_AFTER = 7

def connect_api():
    '''Connect to the API and test connection'''
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '..', 'api.conf'))
    client = CBWApi(conf.get('cyberwatch', 'url'), conf.get(
        'cyberwatch', 'api_key'), conf.get('cyberwatch', 'secret_key'))
    client.ping()
    return client


def find_dockers(client):
    '''Find docker servers and return server_id + creation date'''
    dockers_details = []
    all_dockers = client.docker_images()
    for docker in all_dockers:
        if docker.server_id:
            detail = client.asset(str(docker.server_id))
            dockers_details.append(
                {"server_id": str(docker.server_id), "created_at": detail.created_at})
    return dockers_details


def find_discoveries(client):
    '''Find discoveries with docker images'''
    ids = []
    discoveries_details = client.hosts()
    for host in discoveries_details:
        if host.discovery.type == "CbwAssets::Discovery::DockerRegistry":
            for id in host.server_ids:
                ids.append(str(id))
    return ids


def find_to_clean(dockers, discoveries):
    '''Find docker images to delete'''
    to_clean = []
    for docker in dockers:
        if docker['server_id'] not in discoveries:
            date = datetime.fromisoformat(
                docker['created_at']).replace(tzinfo=None)
            time = datetime.now() - date
            if time.days > DELETE_AFTER:
                to_clean.append(docker)
    return to_clean


def display_and_delete(delete_list, what, client, delete=DELETE):
    '''Display servers then delete them'''
    print('\n\n================= Total of {} {} to delete (delete={}) ================='.format(len(delete_list),
                                                                                                what,
                                                                                                delete))
    for delete_server in delete_list:
        print('{} --- {}'.format(delete_server['server_id'], delete_server['created_at']))
        if delete is True:
            client.delete_server(str(delete_server['server_id']))


def launch_script():
    '''Launch script'''
    client = connect_api()
    dockers = find_dockers(client)
    discoveries = find_discoveries(client)
    clean = find_to_clean(dockers, discoveries)
    display_and_delete(clean, 'docker image', client)

launch_script()
