"""Script used to delete duplicates"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi


def connect_api():
    '''Connect to the API and test connection'''
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '..', 'api.conf'))
    client = CBWApi(conf.get('cyberwatch', 'url'), conf.get(
        'cyberwatch', 'api_key'), conf.get('cyberwatch', 'secret_key'))

    client.ping()
    return client


def find_duplicates(servers):
    '''Find duplicated servers'''
    duplicate = servers[0]
    duplicates = []

    for server in sorted(servers, key=lambda x: (x.hostname is None, x.hostname)):
        if server.hostname == duplicate.hostname and server.hostname is not None:
            if server.last_communication is None or duplicate.last_communication > server.last_communication:
                duplicates.append(server)
            else:
                duplicates.append(duplicate)
                duplicate = server
        else:
            duplicate = server

    return duplicates


def display_and_delete(delete_list, what, client, delete=True):
    '''Display servers then delete them'''
    print('\n\n================= Total of {} {} to delete (delete={}) ================='.format(len(delete_list),
                                                                                                what,
                                                                                                delete))
    for delete_server in delete_list:
        print('{} --- {} --- {} --- {}'.format(delete_server.id, delete_server.hostname,
                                               delete_server.cve_announcements_count, delete_server.created_at))

        if delete is True:
            client.delete_server(str(delete_server.id))


def launch_script():
    '''Launch script'''
    client = connect_api()
    servers = client.servers()

    duplicates = find_duplicates(servers)
    display_and_delete(duplicates, 'duplicates', client)


launch_script()
