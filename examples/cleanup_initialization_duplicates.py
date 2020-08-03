"""Script used to delete duplicates and computers in initialization
To use the script, please install python-dateutil : pip3 install python-dateutil"""

import argparse
import sys
import os

from configparser import ConfigParser
from datetime import datetime
from dateutil.relativedelta import relativedelta  # pylint: disable=import-error
from cbw_api_toolbox.cbw_api import CBWApi

def connect_api():
    '''Connect ot the API'''
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
    global API  # pylint: disable=global-variable-undefined
    API = CBWApi(conf.get('cyberwatch', 'url'), conf.get('cyberwatch', 'api_key'), conf.get('cyberwatch', 'secret_key'))


    API.ping()


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


def find_agents(servers, when):
    '''Find server with agent in initialization status.'''
    agents = []

    agents_date = (datetime.today() - relativedelta(months=+when))
    for server in sorted(servers, key=lambda x: (x.hostname is None, x.hostname)):
        if server.created_at is not None and server.created_at != '':
            if server.status.lower() == 'server_update_init' \
                    and datetime.strptime(server.created_at[:10], '%Y-%m-%d') < agents_date:
                agents.append(server)
        else:
            print('created_at is None for {} -- {}'.format(server.id, server.hostname))

    return agents


def find_agentless(servers, when):
    '''Find agentless server in initialization status.'''
    agentless = []

    agentless_date = (datetime.today() - relativedelta(months=+when))
    for server in sorted(servers, key=lambda x: (x.hostname is None, x.hostname)):
        if server.created_at is not None and server.created_at != '':
            if server.status.lower() == 'server_update_init' \
                    and datetime.strptime(server.created_at[:10], '%Y-%m-%d') < agentless_date:
                agentless.append(server)
        else:
            print('created_at is None for {} -- {}'.format(server.id, server.hostname))

    return agentless

def find_all(servers, agents_time, agentless_time):
    '''Find all servers'''
    duplicate = servers[0]
    duplicates = []
    agentless = []
    agents = []

    for server in sorted(servers, key=lambda x: (x.hostname is None, x.hostname)):
        # Find duplicates
        if server.hostname == duplicate.hostname and server.hostname is not None:
            if server.last_communication is None or duplicate.last_communication > server.last_communication:
                duplicates.append(server)
            else:
                duplicates.append(duplicate)
                duplicate = server
        else:
            duplicate = server

        if server.created_at is not None and server.created_at != '':
            agentless_date = (datetime.today() - relativedelta(months=+agentless_time))
            # Find agentless in initialization for more than X months
            if server.status.lower() == 'server_update_init' \
                    and datetime.strptime(server.created_at[:10], '%Y-%m-%d') < agentless_date:
                agentless.append(server)

            agents_date = (datetime.today() - relativedelta(months=+agents_time))
            # Find agents in initialization for more than X months
            if server.status.lower() == 'server_update_init'\
                    and datetime.strptime(server.created_at[:10], '%Y-%m-%d') < agents_date:
                agents.append(server)

        else:
            print('created_at is None for {} -- {}'.format(server.id, server.hostname))

    return duplicates, agentless, agents

def display_and_delete(delete_list, what, delete=False):
    '''Display servers then delete them'''
    print('\n\n================= Total of {} {} to delete (delete={}) ================='.format(len(delete_list),
                                                                                                what,
                                                                                                delete))
    for delete_server in delete_list:
        print('{} --- {} --- {} --- {}'.format(delete_server.id, delete_server.hostname, \
                    delete_server.cve_announcements_count, delete_server.created_at))

        if delete is True:
            API.delete_server(str(delete_server.id))

def launch_script(parsed_args):
    '''Launch script'''
    connect_api()
    servers = API.servers()

    if parsed_args.duplicates_only:
        duplicates = find_duplicates(servers)
        display_and_delete(duplicates, 'duplicates', parsed_args.duplicates_only)

    elif parsed_args.agents_only:
        agents = find_agents(servers, parsed_args.agents_time)
        display_and_delete(agents, 'agents', parsed_args.agents_only)

    elif parsed_args.agentless_only:
        agentless = find_agentless(servers, parsed_args.agentless_time)
        display_and_delete(agentless, 'agentless connections', parsed_args.agentless_only)

    else:
        duplicates, agentless, agents = find_all(servers, parsed_args.agents_time, parsed_args.agentless_time)
        display_and_delete(duplicates, 'duplicates', parsed_args.delete_all)
        display_and_delete(agentless, 'agentless connections', parsed_args.delete_all)
        display_and_delete(agents, 'agents', parsed_args.delete_all)

def main(args=None):
    '''Main function'''
    if not args:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description='Cleanup script using Cyberwatch API.\nBy default this script is run in read-only mode.')
    parser.add_argument(
        '-da', '--delete_all',
        help='Run the script to delete duplicates, agents and agentless. Time conditions apply to each type',
        action='store_true')
    parser.add_argument(
        '-do', '--duplicates_only',
        help='Delete duplicates only.',
        action='store_true')
    parser.add_argument(
        '-ao', '--agents_only',
        help='Delete agents that haven\'t communicated since the date specified.',
        action='store_true')
    parser.add_argument(
        '-alo', '--agentless_only',
        help='Delete agentless connection that haven\'t communicated since the date specified.',
        action='store_true')
    parser.add_argument(
        '-at', '--agents_time',
        help='Specify the minimal time in months an agent has to be on initialisation before deleting it.',
        default=3, type=int)
    parser.add_argument(
        '-alt', '--agentless_time',
        help='Specify the time in months an agentless connection has to be on initialisation before deleting it.',
        default=6, type=int)

    args = parser.parse_args(args)

    launch_script(args)

if __name__ == '__main__':
    main()
