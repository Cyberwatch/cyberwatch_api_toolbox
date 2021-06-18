"""Script using Cyberwatch API to export hosts with details to XLSX"""

import os
from configparser import ConfigParser
import xlsxwriter
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

def get_node_names(client):
    """Build a list with node and it's details"""
    node_names = {}
    for node in client.nodes():
        node_names[node.id] = node.name
    return node_names

def hosts_details(client):
    """Build a list with each host and it's details"""
    hosts_list = []
    for host in client.hosts():
        host = client.host(str(host.id))
        hosts_list.append(host)
    return hosts_list

def export_xls(client):
    """Export differents categories to the XLSX file"""
    file = xlsxwriter.Workbook('export.xlsx')

    hosts = hosts_details(client)
    computer_tab = file.add_worksheet("Hosts")
    # Create each column
    computer_tab.write(0, 0, "ID")
    computer_tab.write(0, 1, "Hostname")
    computer_tab.write(0, 2, "Address")
    computer_tab.write(0, 3, "Source")
    computer_tab.write(0, 4, "Category")
    computer_tab.write(0, 5, "Associated asset")

    host_details(computer_tab, hosts, get_node_names(client))

    file.close()

def host_details(computer_tab, hosts, nodes):
    """Write each Host and it's details in `Computers` tab"""
    row = 0
    col = 0
    for host in hosts:
        computer_tab.write(row + 1, col, host.id)
        computer_tab.write(row + 1, col + 1, host.hostname)
        computer_tab.write(row + 1, col + 2, host.target)
        computer_tab.write(row + 1, col + 3, nodes[host.node_id])
        computer_tab.write(row + 1, col + 4, host.discovery.type)

        if host.server_ids:
            computer_tab.write(row + 1, col + 5, str(host.server_ids))

        row += 2

def launch_script():
    '''Launch script'''
    client = connect_api()
    export_xls(client)
    print("INFO: Done.")

def main():
    '''Main function'''
    launch_script()


if __name__ == '__main__':
    main()
