"""Script used to delete duplicates and computers in initialization
To use the script, please install python-dateutil : pip3 install python-dateutil"""

import argparse
import sys

from cbw_api_toolbox.cbw_api import CBWApi
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def connect_API():
    API_KEY = ''
    SECRET_KEY = ''
    API_URL = ''

    global API 
    API = CBWApi(API_URL, API_KEY, SECRET_KEY)

    API.ping()

def find_duplicates(servers):
    duplicate = servers[0]
    duplicates = []

    for s in sorted(servers, key=lambda x: (x.hostname is None, x.hostname)):
        if s.hostname == duplicate.hostname and s.hostname is not None:
            if s.last_communication is None or duplicate.last_communication > s.last_communication:
                duplicates.append(s)
            else:
                duplicates.append(duplicate)
                duplicate = s
        else:
            duplicate = s

    return duplicates

def find_agents(servers, when):
    agents = []

    for s in sorted(servers, key=lambda x: (x.hostname is None, x.hostname)):        
        if s.created_at is not None and s.created_at != '':
            if s.status['comment'].lower() == 'initialization' and s.agent_version is not None and datetime.strptime(s.created_at[:10], '%Y-%m-%d') < (datetime.today() - relativedelta(months=+when)):
                agents.append(s)
        else:
            print('created_at is None for {} -- {}'.format(s.id, s.hostname))

    return agents

def find_agentless(servers, when):
    agentless = []

    for s in sorted(servers, key=lambda x: (x.hostname is None, x.hostname)):        
        if s.created_at is not None and s.created_at != '':
            if s.status['comment'].lower() == 'initialization' and s.agent_version is None and datetime.strptime(s.created_at[:10], '%Y-%m-%d') < (datetime.today() - relativedelta(months=+when)):
                agentless.append(s)
        else:
            print('created_at is None for {} -- {}'.format(s.id, s.hostname))

    return agentless

def find_all(servers, agents_time, agentless_time):

    duplicate = servers[0]
    duplicates = []
    agentless = []
    agents = []

    for s in sorted(servers, key=lambda x: (x.hostname is None, x.hostname)):
        # Find duplicates
        if s.hostname == duplicate.hostname and s.hostname is not None:
            if s.last_communication is None or duplicate.last_communication > s.last_communication:
                duplicates.append(s)
            else:
                duplicates.append(duplicate)
                duplicate = s
        else:
            duplicate = s

        if s.created_at is not None and s.created_at != '':
        
            # Find agentless in initialization for more than X months 
            if s.status['comment'].lower() == 'initialization' and s.agent_version is None and datetime.strptime(s.created_at[:10], '%Y-%m-%d') < (datetime.today() - relativedelta(months=+agentless_time)):
                agentless.append(s)

            # Find agents in initialization for more than X months
            if s.status['comment'].lower() == 'initialization' and s.agent_version is not None and datetime.strptime(s.created_at[:10], '%Y-%m-%d') < (datetime.today() - relativedelta(months=+agents_time)):
                agents.append(s)
        
        else:
            print('created_at is None for {} -- {}'.format(s.id, s.hostname))
        
    return duplicates, agentless, agents

def display_and_delete(delete_list, what, delete=False):
    print('\n\n================= Total of {} {} to delete (delete={}) ================='.format(len(delete_list), what, delete))
    for s in delete_list:
        print('{} --- {} --- {} --- {}'.format(s.id, s.hostname, s.cve_announcements_count, s.created_at))
        if delete is True:
            API.delete_server(s.id)

def launch_script(parsed_args):
    connect_API()
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
    if not args:    
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Cleanup script using Cyberwatch API.\nBy default this script is run in read-only mode.')
    parser.add_argument('-da', '--delete_all', help='Run the script to delete duplicates, agents and agentless. Time conditions apply to each type', 
                       action='store_true')
    parser.add_argument('-do', '--duplicates_only', help='Delete duplicates only.', 
                       action='store_true')
    parser.add_argument('-ao', '--agents_only', help='Delete agents that haven\'t communicated since the date specified.', 
                       action='store_true')
    parser.add_argument('-alo', '--agentless_only', help='Delete agentless connection that haven\'t communicated since the date specified.', 
                       action='store_true')
    parser.add_argument('-at', '--agents_time', help='Specify the minimal time in months an agent has to be initialisation for before deleting it.', 
                       default=3, type=int)
    parser.add_argument('-alt', '--agentless_time', help='Specify the minimal time in months an agentless connection has to be initialisation for before deleting it.', 
                       default=6, type=int)

    args = parser.parse_args(args)

    launch_script(args)

if __name__ == '__main__':
    main()

