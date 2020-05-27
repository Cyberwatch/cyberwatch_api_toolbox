"""Find all active /24 subnets present in Cyberwatch and arrange them by nodes"""

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


def ip_per_node(client):
    """Rearrange each ip address with it's specific node"""
    ip_in_nodes = {}
    hosts = client.hosts()

    for node in client.nodes():
        my_list = [x.target for x in hosts if x.node_id == node.id]
        ip_in_nodes[node.name] = my_list
    return ip_in_nodes


def get_all_subnets(ip_in_nodes):
    """Find each ip's subnet, clean duplicates and rearrange each subnet with his node"""
    node_with_subnets = {}
    all_unique_subnets = set()

    for node in ip_in_nodes:
        subnets_list = set()
        for address in ip_in_nodes[node]:
            data = '{}/255.255.255.0'.format(address)
            address = ipaddress.ip_network(
                data, strict=False).__str__()
            all_unique_subnets.add(address)
            subnets_list.add(address)
        node_with_subnets[node] = subnets_list

    print("\nUnique subnets:")
    print(all_unique_subnets)
    return node_with_subnets


def launch_script():
    '''Launch script'''
    client = connect_api()
    ip_in_nodes = ip_per_node(client)
    node_with_subnets = get_all_subnets(ip_in_nodes)
    print("\nNodes with subnets:")
    print(node_with_subnets)


def main(args=None):
    '''Main function'''

    parser = argparse.ArgumentParser(
        description="Script using Cyberwatch API to find all active subnets in /24")

    parser.parse_args(args)
    launch_script()


if __name__ == '__main__':
    main()
