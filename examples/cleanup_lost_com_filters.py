"""Script used to delete server with 'communication_failed' status for 6 months+ (for Cyberwatch 10.2.0+)"""

import os
from configparser import ConfigParser
from datetime import datetime, timedelta
from cbw_api_toolbox.cbw_api import CBWApi

# Asset will be considered for deletion if last communication was  more then MAX_TIME

MAX_TIME = timedelta(days=180)
DELETE_SERVERS = False

def connect_api():
    '''Connect to the API and test connection'''
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '..', 'api.conf'))
    client = CBWApi(conf.get('cyberwatch', 'url'), conf.get(
        'cyberwatch', 'api_key'), conf.get('cyberwatch', 'secret_key'))

    client.ping()
    return client


def find_lost_com_servers(servers):
    '''Filter servers that are "communication_failed" for at least 6 months '''
    lost_com_servers = []
    for server in servers:
        if server.last_communication is not None:
            last_comm_with_delta = datetime.strptime(server.last_communication, '%Y-%m-%dT%H:%M:%S.000%z') + MAX_TIME

            if last_comm_with_delta.replace(tzinfo=None) < datetime.now():

                lost_com_servers.append(server)

    return lost_com_servers


def display_and_delete(delete_list, server_type, client, delete=DELETE_SERVERS):
    '''Display servers then delete them'''
    print('\n\n================ Total of {} {} to delete (delete={}) ================'.format(len(delete_list),
                                                                                                server_type,
                                                                                                delete))
    for delete_server in delete_list:
        print('{} -- {} -- {} -- {}'.format(delete_server.id, delete_server.hostname,
                                               delete_server.cve_announcements_count, delete_server.created_at))

        if delete is True:
            client.delete_server(str(delete_server.id))


def launch_script():
    '''Launch script'''
    client = connect_api()
    filters = {
    "communication_failed": "true"
    }
    servers = client.servers(filters)

    lost_com_servers = find_lost_com_servers(servers)
    display_and_delete(lost_com_servers, 'lost_communication servers', client)


launch_script()
