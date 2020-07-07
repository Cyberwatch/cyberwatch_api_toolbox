"""Fetch servers fixes details by CVE"""

import os
import csv
import logging
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

def to_csv_lines(cve_catalog):
    """Generates a list of dictionnary objects"""
    csv_lines = []
    index_cve = 0
    size_catalog = len(list(cve_catalog))
    for cve in cve_catalog:
        cve_details = CLIENT.cve_announcement(cve.cve_code)
        index_cve += 1
        print("Progress : {}/{} -- {}".format(index_cve, size_catalog, cve.cve_code), end="\r")
        cve_servers = cve_details.servers
        for server in cve_servers:
            server_update = server['server'].updates
            if len(server_update) > 0:
                vendor = "Microsoft" if server_update[0]['target']['type'] == "Packages::Kb" \
                                    else server_update[0]['target']['vendor']
                products_to_fix = ", ".join([server_update[j]['target']['product'] for j in range(len(server_update))
                                             if server_update[j]['target']['product']])
                targets_version = ", ".join([server_update[j]['target']['version'] for j in range(len(server_update))
                                             if server_update[j]['target']['version']])
                csv_lines.append({'Hostname': server['server'].hostname,
                                  'CVE code': cve.cve_code,
                                  'Vendor': vendor,
                                  'CVE score': cve.score_v3,
                                  'Product to fix': products_to_fix.strip(),
                                  'Target version': targets_version.strip()})
    return csv_lines


def to_csv(csv_lines, name_csv='just_generated.csv', path=""):
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

# Fetch active CVE if an exploit is available
logging.info('Fetching active CVE')
cve_list = CLIENT.cve_announcements({"exploitable": "true", "active": "true"})

# Formating lines for the csv
logging.info('Formating lines for the csv file')
csv_lines_list = to_csv_lines(cve_list)

# Exporting csv file
to_csv(csv_lines_list, path="")
