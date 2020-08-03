"""get dashboard indicators"""

from collections import Counter
import os
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

def cve_lists(server_list):
    """Return count of CVE based on access vector"""
    servers = server_list
    cves = CLIENT.cve_announcements({"exploitable": "true", "active": "true"})
    server_cves = {
        'access_vector_network': 0,
        'access_vector_local': 0,
        'access_vector_adjacent': 0,
        'access_vector_physical': 0
    }

    for server in servers:
        server_show = CLIENT.server(str(server.id))
        for cve in server_show.cve_announcements:
            if not(cve.ignored) and cve.fixed_at is None:
                cve_details = next((cve_exploitable for cve_exploitable in
                                    cves if cve_exploitable.cve_code == cve.cve_code), None)

                if cve_details is not None and cve_details.cvss_v3 is not None:
                    server_cves[cve_details.cvss_v3.access_vector] += 1
    return server_cves

def server_outdated_system(servers):
    """Return count of servers which os is not supported by Cyberwatch"""
    return Counter(server.status == "server_not_supported_os" for server in servers)

def server_reboot_required():
    """Return count of server that need reboot"""
    return Counter(server.status == 'server_update_reboot' for server in CLIENT.servers({"reboot_required": "true"}))

def print_results():
    """Presents formatted results"""
    servers = CLIENT.servers()
    cve = cve_lists(servers)
    reboot_required = server_reboot_required()
    outdated_system = server_outdated_system(servers)

    print("{:<45} {:>6}".format("Vulnérabilités avec vecteur d'attaque réseau", cve['access_vector_network']))
    print("{:<45} {:>6}".format("Vulnérabilités avec vecteur d'attaque local", cve['access_vector_local']))
    print("{:<45} {:>6}".format("Actifs nécessitant un redémarrage", reboot_required[True]))
    print("{:<45} {:>6}".format("Actifs ayant un système obsolète", outdated_system[True]))

print_results()
