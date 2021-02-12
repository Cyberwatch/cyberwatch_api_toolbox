"""Add docker image"""

import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

INFO = {
    "image_name": "",  # Mandatory name of docker image on the registry
    "image_tag": "", # Mandatory tag of docker image to analyze
    "docker_registry_id": "", # Mandatory credential ID of the Docker registry to pull from
    "docker_engine_id": "", # Mandatory Credential ID of the Docker engine to run analyzes on.
    "node_id": "", # ID of the Cyberwatch source that will connect to the Docker engine
}

CLIENT.create_docker_image(INFO)
