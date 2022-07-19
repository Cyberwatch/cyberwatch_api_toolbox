"""Upload script result to Cyberwatch for air gapped scans"""

import os
import argparse
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi


def connect_api():
    '''Connect to the API and test connection'''
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..', 'api.conf'))
    client = CBWApi(conf.get('cyberwatch', 'url'), conf.get(
        'cyberwatch', 'api_key'), conf.get('cyberwatch', 'secret_key'))

    client.ping()
    return client


def upload(client):
    """Upload results from the folder 'Uploads' to Cyberwatch"""
    print("INFO: Searching for available results...")
    files = (file for file in sorted(os.listdir(os.path.join(os.path.dirname(__file__), 'Uploads'))))
    for file in files:
        file_path = os.path.join(os.path.dirname(__file__), 'Uploads', file)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding="utf-8") as filehandle:
                filecontent = filehandle.read()
                content = {'output': filecontent, 'groups': 'my_group_1, my_group_2'}
                print('INFO: Sending {} content to the API...'.format(file))
                client.upload_airgapped_results(content)


def launch_script():
    '''Launch script'''
    client = connect_api()
    upload(client)
    print("INFO: Done.")


def main(args=None):
    '''Main function'''

    parser = argparse.ArgumentParser(
        description="Script using Cyberwatch API to upload results from 'Uploads' folder to Cyberwatch")

    parser.parse_args(args)
    launch_script()


if __name__ == '__main__':
    main()
