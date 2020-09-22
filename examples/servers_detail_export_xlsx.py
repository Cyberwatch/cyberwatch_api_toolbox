"""Script using Cyberwatch API to export vulnerabilities of servers with details to XLSX"""

import os
from configparser import ConfigParser
import xlsxwriter
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

def servers_details(client):
    """Build a list with each server and it's details"""
    servers_list = []
    for server in client.servers():
        server = client.server(str(server.id))
        servers_list.append(server)
    return servers_list

def export_xls(client):
    """Export differents categories to the XLSX file"""
    file = xlsxwriter.Workbook('export.xlsx')
    servers = servers_details(client)
    # Create each category tab
    computer_tab = file.add_worksheet("Computers")
    vulnerabilities_tab = file.add_worksheet("Vulnerabilities")
    recommended_tab = file.add_worksheet("Recommended Actions")

    host_details(computer_tab, servers)
    vulnerabilities_details(vulnerabilities_tab, servers, client)
    recommended_actions_details(recommended_tab, servers)

    file.close()

def host_details(computer_tab, servers):
    """Write each Host and it's details in `Computers` tab"""
    row = 0
    col = 0
    for server in servers:
        computer_tab.write(row, col, "Hostname")
        computer_tab.write(row + 1, col, server.hostname)

        computer_tab.write(row, col + 1, "OS")
        computer_tab.write(row + 1, col + 1, server.os.name)

        computer_tab.write(row, col + 2, "Groups")
        if server.groups:
            group_name = ""
            for group in server.groups:
                group_name += group.name + ", "
            group_name = group_name[:-1]
            computer_tab.write(row + 1, col + 2, group_name)

        computer_tab.write(row, col + 3, "Status")
        computer_tab.write(row + 1, col + 3, server.status)

        computer_tab.write(row, col + 4, "Environment")
        computer_tab.write(row + 1, col + 4, server.environment.name)

        computer_tab.write(row, col + 5, "Category")
        computer_tab.write(row + 1, col + 5, server.category)

        row += 3

def vulnerabilities_details(vulnerabilities_tab, servers, client):
    """Write vulnerabilities of each Host and it's details in `Vulnerabilities` tab"""
    row = 0
    col = 0
    for server in servers:
        vulnerabilities_tab.write(row, col, server.hostname)
        row += 1
        vulnerabilities_tab.write(row, col, "Vulnerabilty")
        vulnerabilities_tab.write(row, col + 1, "CVSS score v3")
        vulnerabilities_tab.write(row, col + 2, "CVSS score v2")
        vulnerabilities_tab.write(row, col + 3, "Exploitable")
        vulnerabilities_tab.write(row, col + 4, "Description")
        vulnerabilities_tab.write(row, col + 5, "Access vector v2")
        vulnerabilities_tab.write(row, col + 6, "Access complexity v2")
        vulnerabilities_tab.write(row, col + 7, "Authentication requirement v2")
        vulnerabilities_tab.write(row, col + 8, "Confidentiality impact v2")
        vulnerabilities_tab.write(row, col + 9, "Integrity impact v2")
        vulnerabilities_tab.write(row, col + 10, "Availability impact v2")
        vulnerabilities_tab.write(row, col + 11, "Access vector v3")
        vulnerabilities_tab.write(row, col + 12, "Access complexity v3")
        vulnerabilities_tab.write(row, col + 13, "Privilege requirement v3")
        vulnerabilities_tab.write(row, col + 14, "User Authentication v3")
        vulnerabilities_tab.write(row, col + 15, "Integrity impact v3")
        vulnerabilities_tab.write(row, col + 16, "Availability impact v3")
        vulnerabilities_tab.write(row, col + 17, "Confidentiality impact v3")
        vulnerabilities_tab.write(row, col + 18, "Scope v3")

        # Get details of each CVE
        for cve in server.cve_announcements:
            cve = client.cve_announcement(cve.cve_code)

            vulnerabilities_tab.write(row + 1, col, cve.cve_code)
            vulnerabilities_tab.write(row + 1, col + 1, cve.score_v3)
            vulnerabilities_tab.write(row + 1, col + 2, cve.score_v2)
            vulnerabilities_tab.write(row + 1, col + 3, cve.exploit_code_maturity)
            vulnerabilities_tab.write(row + 1, col + 4, cve.content)

            if cve.cvss is not None:
                vulnerabilities_tab.write(row + 1, col + 5, cve.cvss.access_vector)
                vulnerabilities_tab.write(row + 1, col + 6, cve.cvss.access_complexity)
                vulnerabilities_tab.write(row + 1, col + 7, cve.cvss.authentication)
                vulnerabilities_tab.write(row + 1, col + 8, cve.cvss.availability_impact)
                vulnerabilities_tab.write(row + 1, col + 9, cve.cvss.confidentiality_impact)
                vulnerabilities_tab.write(row + 1, col + 10, cve.cvss.integrity_impact)

            if cve.cvss_v3 is not None:
                vulnerabilities_tab.write(row + 1, col + 11, cve.cvss_v3.access_vector)
                vulnerabilities_tab.write(row + 1, col + 12, cve.cvss_v3.access_complexity)
                vulnerabilities_tab.write(row + 1, col + 13, cve.cvss_v3.privileges_required)
                vulnerabilities_tab.write(row + 1, col + 14, cve.cvss_v3.user_interaction)
                vulnerabilities_tab.write(row + 1, col + 15, cve.cvss_v3.integrity_impact)
                vulnerabilities_tab.write(row + 1, col + 16, cve.cvss_v3.availability_impact)
                vulnerabilities_tab.write(row + 1, col + 17, cve.cvss_v3.confidentiality_impact)
                vulnerabilities_tab.write(row + 1, col + 18, cve.cvss_v3.scope)

            row += 1
        row += 2

def recommended_actions_details(recommended_tab, servers):
    """Write each recommended actions/affected technologies of each Host in `Recommended Actions` tab"""
    row = 0
    col = 0
    for server in servers:
        recommended_tab.write(row, col, server.hostname)
        row += 1

        recommended_tab.write(row, col, "Affected technology")
        recommended_tab.write(row, col + 1, "CVE announcement")
        recommended_tab.write(row, col + 2, "Patchable")
        recommended_tab.write(row, col + 3, "Current version")
        recommended_tab.write(row, col + 4, "Target version")

        for update in server.updates:
            if update.current is not None:
                recommended_tab.write(row + 1, col, update.current.product)
                recommended_tab.write(row + 1, col + 3, update.current.version)
                recommended_tab.write(row + 1, col + 1, ', '.join(update.cve_announcements))
                recommended_tab.write(row + 1, col + 2, update.patchable)
                recommended_tab.write(row + 1, col + 4, update.target.version)
            else:
                recommended_tab.write(row + 1, col, update.target.product)
                recommended_tab.write(row + 1, col + 1, ', '.join(update.cve_announcements))
                recommended_tab.write(row + 1, col + 2, update.patchable)

            row += 1
        row += 2


def launch_script():
    '''Launch script'''
    client = connect_api()
    export_xls(client)
    print("INFO: Done.")

def main():
    '''Main function'''
    launch_script()


if __name__ == '__main__':
    main()
