"""
Example script for sending data to Qradar.
Please provide a qradar url in your api.conf file using this format:

[qradar]
url = http://[QRADAR_URL]:[HTTP_RECEIVER_PORT]
"""

import argparse
from argparse import RawTextHelpFormatter
import os
import json
from configparser import ConfigParser
import requests
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


def get_url():
    '''Get Qradar url from api.conf'''
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '..', 'api.conf'))
    client = conf.get('qradar', 'url')

    return client


def post_qradar(server, code_list):
    '''Send a post request to Qradar HTTP Receiver'''
    headers = {'Content-Type': 'application/json'}

    payload = {
        "EventCategory": "Cyberwatch Integration",
        "Hostname": server.hostname,
        "Status": server.status,
        "Vulnerabilities": code_list
    }

    res = requests.post(url=get_url(), headers=headers,
                        data=json.dumps(payload), verify=False)
    res.raise_for_status()
    return res.status_code


def cve_code_list(server_id, client):
    '''Build CVE Code list'''
    server = client.server(str(server_id))
    return list(map(lambda x: x.cve_code, server.cve_announcements))


def launch_script():
    '''Launch script'''
    client = connect_api()
    servers = client.servers()
    for server in servers:
        post_qradar(server, cve_code_list(server.id, client))


def main(args=None):
    '''Main function'''

    parser = argparse.ArgumentParser(
        description="""Script using Cyberwatch API to send a Post request for each servers to Qradar HTTP Receiver.
Please provide a qradar url in your api.conf file using this format:
    [qradar]
    url = http://[QRADAR_URL]:[HTTP_RECEIVER_PORT]""", formatter_class=RawTextHelpFormatter)

    parser.parse_args(args)
    launch_script()


if __name__ == '__main__':
    main()
