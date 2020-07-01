"""get dashboard indicators"""

from collections import Counter
import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

def cve_lists():
    """Return count of CVE based on access vector"""
    list_cve = CLIENT.cve_announcements({"exploitable": "true", "active": "true"})
    return Counter(cve.cvss_v2['access_vector'] if cve.cvss_v2 is not None else None for cve in list_cve)

def server_outdated_system():
    """Return count of servers which os is not supported by Cyberwatch"""
    servers = CLIENT.servers()
    return Counter(server.status == "server_not_supported_os" for server in servers)

def server_reboot_required():
    """Return count of server that need reboot"""
    return len(CLIENT.servers({"reboot_required": "false"}))

def print_results():
    """Presents formatted results"""

    cve = cve_lists()
    reboot_required = server_reboot_required()
    outdated_system = server_outdated_system()

    print("{:<45} {:>6}".format("Vulnérabilité avec  vecteur d'accès réseau", cve['access_vector_network']))
    print("{:<45} {:>6}".format("Vulnérabilités avec vecteur d'accès local", cve['access_vector_local']))
    print("{:<45} {:>6}".format("Actifs nécessitant un redémarrage", reboot_required))
    print("{:<45} {:>6}".format("Actifs ayant un système obsolète", outdated_system['server_not_supported_os']))

print_results()
