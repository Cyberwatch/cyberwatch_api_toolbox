"""Get all linux hosts with port 22 open in specified subnets and create an agentless connection if not supervised """

import os
import ipaddress
import argparse
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


# Change these variables to NOT use the default credentials for SSH set up in Cyberwatch
SSH_LOGIN = ""
SSH_PASSWORD = ""

NEW = []
EXISTING = []
ERRORS = []


def create_agentless(host, client, parsed_args):
    """Create an agentless connection if not in read-only"""
    info = {"type": "CbwRam::RemoteAccess::Ssh::WithPassword",
            "address": host.target,
            "port": "22",
            "node_id": host.node_id,
            "login": SSH_LOGIN,
            "password": SSH_PASSWORD
            }
    if parsed_args.i is True:
        create = client.create_remote_access(info)
        if create is False:
            ERRORS.append(host)
        else:
            NEW.append(create)
    else:
        NEW.append(host.target)


def add_hosts_all_subnets(client, parsed_args):
    """Get all linux hosts with port 22 open, without checking the subnet and add them if not in read-only"""
    for host in client.hosts():
        if host.category == "linux":
            if host.server_id:
                EXISTING.append(host)
            if host.server_id is None:
                create_agentless(host, client, parsed_args)


def add_hosts_specific_subnet(client, parsed_args):
    """Get all linux hosts with port 22 open, check if hosts are in specified subnets and add them if importing"""
    for host in client.hosts():
        if host.category == "linux":
            for subnet in parsed_args.subnet:
                if ipaddress.IPv4Address(host.target) in ipaddress.IPv4Network(subnet):
                    if host.server_id:
                        EXISTING.append(host)
                    if host.server_id is None:
                        create_agentless(host, client, parsed_args)


def display(already_supervised, new_connections, error_list, parsed_args):
    '''Display servers for logging purpose'''

    print('\n\n================= Total of {} already supervised servers ================='.format(
        len(already_supervised)))

    for server in already_supervised:
        print('{} --- {}'.format(server.target,
                                 server.server_id))

    print('\n\n================= Total of {} new agentless connections (Importing={})================='.format(
        len(new_connections), parsed_args.i))

    for agentless in new_connections:
        if parsed_args.i is False:
            print('{}'.format(agentless))
        else:
            print('{} --- {}'.format(agentless.address,
                                     agentless.id))

    print('\n\n================= Total of {} errors ================='.format(
        len(error_list)))
    print('\nErrors can happens when, for example, the agentless connection already exists but the associated server')
    print('has not been created because the connection credentials or some other prerequisites are invalid.\n')

    for error in error_list:
        print('{}'.format(error.target))


def launch_script(parsed_args):
    '''Launch script'''
    if parsed_args.subnet != []:
        try:
            for subnet in parsed_args.subnet:
                ipaddress.ip_network(subnet, strict=False)
        except ValueError as v_error:
            raise ValueError("Please provide valid subnet") from v_error

    client = connect_api()
    if parsed_args.subnet == []:
        add_hosts_all_subnets(client, parsed_args)
    else:
        add_hosts_specific_subnet(client, parsed_args)
    display(EXISTING, NEW, ERRORS, parsed_args)


def main(args=None):
    '''Main function'''

    parser = argparse.ArgumentParser(
        description="""Script using Cyberwatch API to find linux hosts in specifics subnets and add them as an agentless
         connection if it's not monitored already.
         By default this script is run in read-only mode and on all subnets""")

    parser.add_argument(
        '-i',
        help='Import found not monitored linux hosts to Cyberwatch.', default=False,
        action='store_true')

    parser.add_argument(
        "--subnet",
        nargs="*",
        type=str,
        help="Specify one or more subnets to look for linux hosts. For example : '--subnet 10.10.0.0/24 172.18.0.0/24'",
        default=[],
    )

    args = parser.parse_args(args)
    launch_script(args)


if __name__ == '__main__':
    main()
