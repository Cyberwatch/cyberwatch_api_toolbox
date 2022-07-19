"""Create remote access"""

import os
import json
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

def match_system_cyberwatch(system):
    """Function used to match the system specified in the file with Cyberwatch syntax"""
    if system == "windows":
        return "CbwRam::RemoteAccess::WinRm::WithNegotiate", 5985
    if system == "linux":
        return "CbwRam::RemoteAccess::Ssh::WithPassword", 22
    if system == "network device":
        return "CbwRam::RemoteAccess::Snmp", 161
    print("System '{}' not recognized, setting default as 'Linux' and port 22".format(system))
    return "CbwRam::RemoteAccess::Ssh::WithPassword", 22


def parse_json_file(json_file_path):
    """Parse the json file specified and create remote access objects in Cyberwatch"""
    # Set default values for the source (node_id) and the credential in case they are not specified
    remote_access_infos = {
        "address": "",
        "type": "",
        "port": "",
        "credential_id": "4",
        "node_id": "1",
        "server_groups": ""
    }

    # Parse the json file, we assume "host" and "system" are mandatory values
    with open(json_file_path, encoding="utf-8") as json_data:
        data = json.load(json_data)
        for json_dict in data:
            remote_access_infos["address"] = json_dict["host"]
            # Get system and set default port value based on the system
            remote_access_infos["type"], remote_access_infos["port"] = match_system_cyberwatch(json_dict["system"])
            # If the port is defined is the json, use its value to override else keep the default value
            remote_access_infos["port"] = json_dict.get("port", remote_access_infos["port"])

            remote_access_infos["credential_id"] = json_dict.get("credential_id", remote_access_infos["credential_id"])
            remote_access_infos["node_id"] = json_dict.get("node_id", remote_access_infos["node_id"])
            remote_access_infos["server_groups"] = json_dict.get("cyberwatch_groups",
                                                                 remote_access_infos["server_groups"])

            print("Trying to create Cyberwatch remote access with the following information : {}"
                  .format(remote_access_infos))
            CLIENT.create_remote_access(remote_access_infos)

JSON_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'example.json')
parse_json_file(JSON_FILE)
