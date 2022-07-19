"""Retrieves information from OCS Iventory API to create air-gap assets in Cyberwatch"""

import os
import re
import json
from configparser import ConfigParser
import requests
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..', 'api.conf'))

def connect_cyberwatch_api():
    '''Connect to the Cyberwatch API and test the connection'''
    client = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'),
                    CONF.get('cyberwatch', 'secret_key'))

    client.ping()
    return client

def request_to_json(url):
    '''Request to self signed OCS Inventory URL and return json object'''
    request = requests.get(url, verify=False)
    json_request = json.loads(request.text)
    return json_request

def create_infoscript(computer, computer_id):
    '''Generates the Cyberwatch infoscript'''
    print('Generating Infoscript for OCS ID: {}'.format(computer_id))
    # Try to identify if the system is Windows or macOS, default is Unix
    system_type = 'unix'
    identifier_script_value = '0'
    if re.search('windows', computer[computer_id]['hardware']['OSNAME'], re.IGNORECASE):
        system_type = 'windows'
        identifier_script_value = '1'
    elif re.search('macos', computer[computer_id]['hardware']['OSNAME'], re.IGNORECASE):
        system_type = 'macos'
        identifier_script_value = '5'

    # Write in the infoscript
    with open(os.path.join(os.path.dirname(__file__), 'ocs_export', '{}_infoscript.txt'
                           .format(computer_id)), 'w', encoding="utf-8") as infoscript:
        infoscript.write('IDENTIFIER_SCRIPT:{}'.format(identifier_script_value)+'\n')
        infoscript.write('IDENTIFIER_HOSTNAME:{}'.format(computer[computer_id]['hardware']['NAME'])+'\n')
        infoscript.write('HOSTNAME:{}'.format(computer[computer_id]['hardware']['NAME'])+'\n')
        # Architecture : always set as x64 but could be better handled if we have the information in OCS
        arch = computer[computer_id]['hardware']['ARCH']
        if system_type == 'windows':
            arch = 'AMD64'
        else:
            arch = 'x86_64'
        infoscript.write('ARCH:{}'.format(arch)+'\n')
        infoscript.write('OS_PRETTYNAME:{}'.format(computer[computer_id]['hardware']['OSNAME'])+'\n')
        if system_type in'unix' or system_type in 'macos':
            infoscript.write('KERNEL_VERSION:{}'.format(computer[computer_id]['hardware']['OSVERSION'])+'\n')
        elif system_type == 'windows':
            # Set OS_VERSION, OS_BUILD and WUA_VERSION as hardcoded values since OCS does not provide this information
            infoscript.write('OS_VERSION:2009'+'\n')
            infoscript.write('OS_BUILD:19042.746'+'\n')
            infoscript.write('WUA_VERSION:10.0.19041.800'+'\n')
    print('Created file {}'.format(infoscript.name))

    return system_type

def create_windows_packagesscript(computer, computer_id):
    '''Generates the Cyberwatch packagesscript for Windows systems'''
    # For Windows systems, create a packagesscript file
    filename = '{}_packagesscript.txt'.format(computer_id)
    softwares = computer[computer_id]['softwares']
    with open(os.path.join(os.path.dirname(__file__), 'ocs_export', filename), 'w', encoding="utf-8") as packagesscript:
        packagesscript.write('IDENTIFIER_SCRIPT:2'+'\n')
        packagesscript.write('IDENTIFIER_HOSTNAME:{}'.format(computer[computer_id]['hardware']['NAME'])+'\n')

        for software in softwares:
            # Identify if the software is a Microsoft KB or regular application
            microsoft_kb = re.findall('KB[0-9]{6,}', software['NAME'])
            if microsoft_kb:
                packagesscript.write('PACKAGE:{}'.format(microsoft_kb[0])+'\n')
            else:
                packagesscript.write('APPLICATION:{}|{}'.format(software['NAME'], software['VERSION'])+'\n')

    print('Created file {}'.format(packagesscript.name))

def create_general_packagesscript(computer, computer_id):
    '''Generates the Cyberwatch packagesscript'''
    # If system is macos or unix, we write packages in infoscript
    filename = '{}_infoscript.txt'.format(computer_id)
    softwares = computer[computer_id]['softwares']
    with open(os.path.join(os.path.dirname(__file__), 'ocs_export', filename), 'a', encoding="utf-8") as packagesscript:
        for software in softwares:
            packagesscript.write('PACKAGE:{}|{}'.format(software['NAME'], software['VERSION'])+'\n')

    print('Appended file {}'.format(packagesscript.name))

def create_empty_portsscript(computer, computer_id, identifier_id):
    '''Generates empty Cyberwatch portsscript to avoid status awaiting analysis'''
    filename = '{}_portsscript.txt'.format(computer_id)
    with open(os.path.join(os.path.dirname(__file__), 'ocs_export', filename), 'w', encoding="utf-8") as portsscript:
        portsscript.write('IDENTIFIER_SCRIPT:{}'.format(identifier_id)+'\n')
        portsscript.write('IDENTIFIER_HOSTNAME:{}'.format(computer[computer_id]['hardware']['NAME'])+'\n')
        #portsscript.write('TCP:135'+'\n')

def export_ocs():
    '''Create text files to be imported in Cyberwatch using all OCS Inventory'''
    ocs_url = CONF.get('ocs_inventory', 'url')

    # Get a list of all the computer IDs
    list_id = request_to_json(ocs_url+'computers/listID')
    print(list_id)

    for computer_id in list_id:
        computer = request_to_json(ocs_url+'computer/{}'.format(computer_id['ID']))
        system_type = create_infoscript(computer, str(computer_id['ID']))

        if system_type == 'windows':
            create_windows_packagesscript(computer, str(computer_id['ID']))
            create_empty_portsscript(computer, str(computer_id['ID']), '11')
        elif system_type == 'unix':
            create_general_packagesscript(computer, str(computer_id['ID']))
            create_empty_portsscript(computer, str(computer_id['ID']), '10')
        elif system_type == 'macos':
            create_general_packagesscript(computer, str(computer_id['ID']))

def upload_cyberwatch(client):
    """Upload results from the folder 'ocs_export' to Cyberwatch"""
    print('INFO: Searching for available results...')
    files = (file for file in sorted(os.listdir(os.path.join(os.path.dirname(__file__), 'ocs_export'))))
    for file in files:
        file_path = os.path.join(os.path.dirname(__file__), 'ocs_export', file)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding="utf-8") as filehandle:
                filecontent = filehandle.read()
                content = {'output': filecontent, 'groups': 'OCS_Inventory'}
                print('INFO: Sending {} content to the API...'.format(file))
                client.upload_airgapped_results(content)
                print('INFO: Done.')

export_ocs()
upload_cyberwatch(connect_cyberwatch_api())
