"""Create remote access"""

from cbw_api_toolbox.cbw_api import CBWApi

API_KEY = 'VxtADOcHiWajDas8/aAFn6Gu/watykEsxm31FgpdvXI='
SECRET_KEY = 'Un0LyCnP78ISCh/N+cLdWDjUvIo7QwcVNWOczYg30fMeEZ3xTVo8DK31zfI3Ywneglpx9UO56AgnfRi/XlX+Og=='
API_URL = 'https://edge.cyberwatch.fr'

CLIENT = CBWApi(API_URL, API_KEY, SECRET_KEY)

INFO = {"type": "", #mandatory, precises the type of the connection
        "address": "", #mandatory, precises the IP address or the domain name of the targeted computer
        "port": "", #mandatory, precises the port of the connection
        "login": "", #mandatory, precises the login of the connection
        "password": "", #precises the password of the connection
        "key": "", #precises the key of the connection
        "node": "", #precises the Cyberwatch source of the connection
        "server_groups": "" #precise the group of the connection
        }

CLIENT.create_remote_access(INFO)
