"""Servers CVEs from group to CSV"""

import os
import csv
import logging
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

# Find the ID on [CYBERWATCH_URL]/cbw_assets/groups and edit the concerned stored credential (the ID will be in the URL)
# Example: "https://[CYBERWATCH_URL]/cbw_assets/groups/9/edit" the GROUP_ID is '9'
GROUP_ID = ""

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

def to_csv(csv_lines, name_csv, path=""):
    """Write objects in csv_lines into a csv file"""
    with open(os.path.join(path, name_csv), 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['"sep=,"'])
        fieldnames = csv_lines[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for line in csv_lines:
            writer.writerow(line)


def to_csv_lines(server_list):
    """Generates a list of dictionnary objects"""
    for server in server_list:
        csv_lines = []
        index_cve = 0
        if server.cve_announcements_count > 0:
            Z = CLIENT.server(str(server.id))
            index_cve += 1
            for cve in Z.cve_announcements:
                csv_lines.append({"Vulnérabilité": cve.cve_code,
                                    "Dernière analyse de l'actif": Z.analyzed_at,
                                    "Score CVSS": cve.score,
                                    "Vulnérabilité prioritaire": cve.prioritized,
                                    "Date de détection": cve.detected_at,
                                    "Ignorée": cve.ignored,
                                    "Commentaire": cve.comment
                })

        logging.info('Generating ' + server.hostname + '.csv')
        to_csv(csv_lines,name_csv=server.hostname + ".csv", path="")

    return None

logging.info('Fetching Servers')
servers_in_group = CLIENT.servers({"group_id": GROUP_ID})
to_csv_lines(servers_in_group)

