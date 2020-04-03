"""Script used to import not monitored servers from cloud into Cyberwatch and delete terminated cloud servers"""

# Based on the Apache Libcloud API https://libcloud.apache.org/index.html
# Tested on Google Compute Engine and AWS EC2

# Prerequisites :
# - Install libcloud with command "pip3 install apache-libcloud"
# - If you are not using the default credentials for agentless connections configured in Cyberwatch, set up SERVER_LOGIN and/or WINRM_password variables
# - Set the constant variables on the first lines of the script depending on which cloud provider you use (https://libcloud.readthedocs.io/en/stable/compute/drivers/)
# - Set up your Cyberwatch API key in api.conf in the same folder as the script, for an example https://github.com/Cyberwatch/cyberwatch_api_toolbox#configuration
# - SSH key file of servers to import named "id_rsa"
# Notes :
# - All servers will be imported with group "cloud_crawling" + zone (ex: "europe-west4-a")

import argparse
import os
import socket

from configparser import ConfigParser
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from cbw_api_toolbox.cbw_api import CBWApi

SSH_KEY_SERVERS = open(os.path.expanduser('id_rsa')).read()
SERVER_LOGIN = ""
WINRM_PASSWORD_SERVERS = ""

# GCE
GCE_EMAIL = ""
GCE_FILE = ""
GCE_PROJECT_ID = ""
# EC2
EC2_ACCESS_KEY = ""
EC2_SECRET_KEY = ""
EC2_REGION = ""

def connect_api():
    '''Connect to the API and test connection'''
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '.', 'api.conf'))
    global API  # pylint: disable=global-variable-undefined
    API = CBWApi(conf.get('cyberwatch', 'url'), conf.get(
        'cyberwatch', 'api_key'), conf.get('cyberwatch', 'secret_key'))

    API.ping()


def get_node():
    '''Get list of available nodes and prompt user to choose'''
    nodes = API.nodes()
    if len(nodes) > 1 :
        print("Which Cyberwatch node do you want to use to import?")
        for node in nodes:
            print("ID: {}, name: {}".format(node.id, node.name))

        node_id = int(input("Enter ID of node to use : "))

        if node_id in [node.id for node in nodes]:
            return node_id
        else:
            raise ValueError("Please provide valid node id")
    else: 
        return nodes[0].id


def retrieve_gce_servers():
    '''Retrieve running GCE servers with apache-libcloud'''
    running = []
    compute_engine = get_driver(Provider.GCE)
    # driver = compute_engine('your_service_account_email', 'path_to_gce_key_file', project='your_project_id')
    driver = compute_engine(GCE_EMAIL, GCE_FILE, project=GCE_PROJECT_ID)
    for server in driver.list_nodes():
        if server.state == "running":
            groups = "cloud_crawling" ", " + server.extra['zone'].name
            if server.extra.get('labels') is not None:
                if "group" in server.extra['labels']:
                    groups += ", " + server.extra['labels']["group"]
            server.extra['server_groups'] = groups
            running.append(server)
    return running


def retrieve_ec2_servers():
    '''Retrieve running ec2 servers with apache-libcloud'''
    running = []
    compute_engine = get_driver(Provider.EC2)
    # driver = compute_engine(ACCESS_ID, SECRET_KEY, region="")
    driver = compute_engine(EC2_ACCESS_KEY, EC2_SECRET_KEY, region=EC2_REGION)
    for server in driver.list_nodes():
        if server.state == "running":
            groups = "cloud_crawling" + ", " + server.extra['availability']
            if server.extra.get('tags') is not None:
                if "group" in server.extra['tags']:
                    groups += ", " + server.extra['tags']["group"]
            server.extra['server_groups'] = groups
            running.append(server)
    return running


def port_checker(ip, port):
    '''Check if a specific port is open on an ip address'''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False


def check_add_server(servers, cloud_servers, node_id):
    '''Find cloud servers not monitored in Cyberwatch to import'''
    to_add = []
    for cloud_server in cloud_servers:
        cloud_server_ip = cloud_server.public_ips[0]
        if not any(server.address == cloud_server_ip for server in servers):
            info = {}
            # Add server information
            info.update({"login": SERVER_LOGIN, "address": cloud_server_ip,
                         "node_id": node_id, "server_groups": cloud_server.extra['server_groups']})
            # Check port and add connection type
            if port_checker(cloud_server_ip, 5985):
                info.update({"type": "CbwRam::RemoteAccess::WinRm::WithNegotiate",
                             "port": 5985})
                info.update({"password": WINRM_PASSWORD_SERVERS})
                to_add.append(info)
            elif port_checker(cloud_server_ip, 22):
                info.update({"type": "CbwRam::RemoteAccess::Ssh::WithKey", "port": 22,
                             "key": SSH_KEY_SERVERS})
                to_add.append(info)
            else:
                print('The server ' + cloud_server_ip + ' has no default port exposed (SSH/22 or WINRM/5985) so an agentless connection with Cyberwatch is not possible')
    return to_add


def check_delete_server(cloud_servers):
    '''Find not imported cloud servers to delete'''
    to_delete = []
    servers = API.servers()
    for server in servers:
        if not any(cloud_server.public_ips[0] == server.remote_ip for cloud_server in cloud_servers):
            for group in server.groups:
                if group.name == "cloud_crawling":
                    to_delete.append(server)
    return to_delete


def display_and_import(to_import_list, apply=False):
    '''Display to_import servers then import them'''

    print('\n\n================= Total of {} cloud servers to import (apply={}) ================='.format(len(to_import_list),
                                                                                                           apply))
    for to_add_server in to_import_list:
        print('{} --- {} --- {}'.format(to_add_server["address"],
                                        to_add_server["server_groups"], to_add_server["type"]))
        if apply is True:
            API.create_remote_access(to_add_server)


def display_and_delete(to_delete_list, apply=False):
    '''Display to_delete servers then delete them'''
    print('\n\n================= Total of {} servers on Cyberwatch to delete (apply={}) ================='.format(len(to_delete_list),
                                                                                                                   apply))
    for server in to_delete_list:
        print('{} --- {} --- {}'.format(server.remote_ip, server.hostname, server.id))
        if apply is True:
            API.delete_server(str(server.id))


def launch_script(parsed_args):
    '''Launch script'''
    connect_api()
    servers = API.remote_accesses()

    if parsed_args.cloud_provider.lower() == "gce":
        cloud_servers = retrieve_gce_servers()
    elif parsed_args.cloud_provider.lower() == "ec2":
        cloud_servers = retrieve_ec2_servers()
    else:
        raise ValueError("Please provide valid cloud_provider argument")

    if parsed_args.a is True:
        if parsed_args.i is False and parsed_args.d is False:
            parsed_args.i = True
            parsed_args.d = True
    elif parsed_args.i is False and parsed_args.d is False:
        print("Read-only")
        parsed_args.i = True
        parsed_args.d = True
    else:
        print("Read-only")

    if parsed_args.i:
        node_id = get_node()
        display_and_import(check_add_server(servers, cloud_servers, node_id), parsed_args.a)
    if parsed_args.d:
        display_and_delete(check_delete_server(cloud_servers), parsed_args.a)

def main(args=None):
    '''Main function'''

    parser = argparse.ArgumentParser(
        description='Script using Cyberwatch API to import not monitored cloud servers and delete terminated cloud servers in Cyberwatch.\nBy default this script is run in read-only mode.')

    parser.add_argument(
        '-i',
        help='Find not monitored cloud servers in Cyberwatch', default=False,
        action='store_true')

    parser.add_argument(
        '-d',
        help='Find terminated cloud servers to delete from Cyberwatch.', default=False,
        action='store_true')

    parser.add_argument(
        '-a',
        help='Apply previewed changes to Cyberwatch by creating remote accesses or removing assets', default=False,
        action='store_true')

    parser.add_argument('cloud_provider', metavar='cloud_provider', type=str,
                        help='Determine cloud provider (EC2 or GCE)')

    args = parser.parse_args(args)
    launch_script(args)


if __name__ == '__main__':
    main()
