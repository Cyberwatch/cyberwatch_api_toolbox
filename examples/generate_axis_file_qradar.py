"""
Example script for generating AXIS file used by QRadar
Please provide cyberwatch server information in your api.conf file using this format:

[qradar]
cyberwatch_ip = [CYBERWATCH_SERVER_IP]
cyberwatch_hostname = [CYBERWATCH_SERVER_HOSTNAME]
cyberwatch_user = [CYBERWATCH_USER]
cyberwatch_version = [CYBERWATCH_VERSION]
"""

import os
import sys
from configparser import ConfigParser
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(
    os.path.dirname(__file__)), '.', 'api.conf'))

def connect_api():
    '''Connect to the API and test connection'''
    client = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get(
        'cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))
    client.ping()
    return client

def get_server_info(server_id, client):
    '''Get server information'''
    server = client.server(str(server_id))
    return server

def get_asset_info(server_id, client):
    '''Get asset information'''
    asset = client.asset(str(server_id))
    return asset

def add_metadata(asset, server_metadata, host):
    '''Hardware profile (metadata)'''
    metadata = asset.metadata
    for meta in metadata:
        server_metadata[meta.key] = meta.value
    if server_metadata:
        hardware = ET.SubElement(host, 'hardwareProfile')
        if server_metadata.get('system-manufacturer') and server_metadata.get('system-model'):
            ET.SubElement(hardware, 'hardwareItem', {'type': 'system', 'manufacturer': server_metadata.get(
                'system-manufacturer'), 'name': server_metadata.get('system-model'), 'serial': '1111111111'})

        if server_metadata.get('system-manufacturer') and server_metadata.get('system-product-name'):
            ET.SubElement(hardware, 'hardwareItem', {'type': 'system', 'manufacturer': server_metadata.get(
                'system-manufacturer'), 'name': server_metadata.get(
                    'system-product-name'), 'serial': server_metadata.get('system-serial-number')})

        if server_metadata.get('processor-manufacturer') and server_metadata.get('processor-version'):
            ET.SubElement(hardware, 'hardwareItem', {'type': 'processor', 'manufacturer': server_metadata.get(
                'processor-manufacturer'), 'name': server_metadata.get('processor-version'), 'serial': '2222222'})

        if server_metadata.get('processor-model-name'):
            ET.SubElement(hardware, 'hardwareItem', {'type': 'processor', 'manufacturer': str(server_metadata.get(
                'processor-model-name')).split()[0], 'name': server_metadata.get(
                    'processor-model-name'), 'serial': '333333333'})
    server_metadata.clear()

def create_xml():
    '''Create XML file'''

    client = connect_api()
    servers = client.servers()
    server_metadata = {}

    root = ET.Element("scanReport")

    #--------------
    #SCANNER BRANCH
    #--------------
    scanner = ET.SubElement(root, "identifyingScanner")

    #scannerIp --required
    ET.SubElement(scanner, 'scannerIp', {'type': 'IPv4', 'value' : CONF.get('qradar', 'cyberwatch_ip')})

    #scannerName --required
    ET.SubElement(scanner, 'scannerName').text = CONF.get('qradar', 'cyberwatch_hostname')

    #scannerVendor --optional
    ET.SubElement(scanner, 'scannerVendor').text = 'Cyberwatch'

    #scannerVersion --optional
    ET.SubElement(scanner, 'scannerVersion').text = CONF.get('qradar', 'cyberwatch_version')

    #scannerUser --required
    ET.SubElement(scanner, 'scannerUser').text = CONF.get('qradar', 'cyberwatch_user')

    #scannerExportTime --required
    now = datetime.now()
    ET.SubElement(scanner, 'scannerExportTime').text = str(now)

    #------------
    # HOST BRANCH
    #------------
    for server_from_index in servers:
        server = get_server_info(server_from_index.id, client)
        asset = get_asset_info(server_from_index.id, client)

        host = ET.SubElement(root, "host")

        #IP
        if len(server.addresses) != 0:
            ET.SubElement(host, 'ip', {'type': 'IPv4', 'value' : server.addresses[-1]})
        else:
            ET.SubElement(host, 'ip', {'type': 'IPv4', 'value' : ""})

        #Hostname
        ET.SubElement(host, 'hostname').text = server.hostname

        #OS
        if server.os is not None:
            ET.SubElement(host, 'operatingSystem', {'name': server.os.name, 'version': server.os.short_name})
        else:
            ET.SubElement(host, 'operatingSystem', {'name': ""})

        #Last communication
        ET.SubElement(host, 'lastSeen').text = server.last_communication

        add_metadata(asset, server_metadata, host)

        #Open ports and associated services - if exist
        for server_port in asset.ports:
            port = ET.SubElement(host, 'port', {'value' : str(server_port.port), 'protocol': server_port.protocol})
            if server_port.package is not None:
                ET.SubElement(port, 'service', {'name': str(server_port.package.product), 'vendor': str(
                    server_port.package.vendor), 'version': str(server_port.package.version)})

        #Vulnerabilities
        for vul in server.cve_announcements:
            ET.SubElement(host, 'vulnerability', {'type': 'CVE ID', 'id': str(vul.cve_code), 'risk': str(vul.score)})

        #Applications
        for package in asset.packages:
            ET.SubElement(host, 'application', {'name': str(package.product), 'vendor': str(
                package.vendor), 'version': str(package.version)})

    # Formatage des données
    formated_xml = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ", encoding='utf-8').strip()

    with open(os.path.join(sys.path[0], "axis_cyberwatch.xml"), "wb") as file:
        file.write(formated_xml)

create_xml()
