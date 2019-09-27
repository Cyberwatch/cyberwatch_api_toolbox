"""Create remote access"""

from cbw_api_toolbox.cbw_api import CBWApi

API_KEY = ''
SECRET_KEY = ''
API_URL = ''
INFO = {"type": "", #mandatory, precises the type of the connection
        "address": "", #mandatory, precises the IP address or the domain name of the targeted computer
        "port": "", #mandatory, precises the port of the connection
        "login": "", #mandatory, precises the login of the connection
        "password": "", #precises the password of the connection
        "key": "", #precises the key of the connection
        "node": "" #precises the Cyberwatch source of the connection
        }

CLIENT = CBWApi(API_URL, API_KEY, SECRET_KEY)

CLIENT.create_remote_access(INFO)
