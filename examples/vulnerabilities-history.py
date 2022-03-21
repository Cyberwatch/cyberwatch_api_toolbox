"""Generate a CSV file containing a summary of detected/corrected/active vulnerabilities of a group of assets"""

import os
import csv
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(
    os.path.dirname(__file__)), '..', 'api.conf'))

print("! Testing communication with Cyberwatch API")
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get(
    'cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))
API_URL = CONF.get('cyberwatch', 'url')

CLIENT.ping()

############################################################
# CONFIGURATION - USE THIS SECTION TO CUSTOMIZE YOUR REPORTS
############################################################

CVE_FILTERS = {
    "groups": ["", ""] # ( ["group"] or ["groupA", "groupB", "groupC"]...)
}

############################################################

cve_announcements = CLIENT.cve_announcements(CVE_FILTERS)

fieldnames = ['Hostname', 'CVE', 'Score', 'Sévérité', 'Date de détection', 'Date de correction']

with open('path/to/csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for cve in cve_announcements:
        cve_details = CLIENT.cve_announcement(str(cve.cve_code))
        for server in cve_details.servers:
            writer.writerow({'Hostname': server.hostname, 'CVE': cve.cve_code,'Score':cve.score, 'Sévérité': cve.level, 'Date de détection': server.detected_at, 'Date de correction': server.fixed_at})
