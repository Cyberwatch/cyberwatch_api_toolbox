"""Example: export vulnerabilities to XLSX"""

import os
from configparser import ConfigParser
import xlsxwriter  # pylint: disable=import-error
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

CLIENT.ping()

SERVERS = CLIENT.servers()

EXPORTED = xlsxwriter.Workbook('export.xlsx')

# Create each category tab
COMPUTER = EXPORTED.add_worksheet("Computers")
VULNERABILITIES = EXPORTED.add_worksheet("Vulnerabilities")
SECURITY = EXPORTED.add_worksheet("Security Advisories")
RECOMMENDED = EXPORTED.add_worksheet("Recommended Actions")

# Build a list with each server and it's details
SERVERS_LIST = []
for server in SERVERS:
    server = CLIENT.server(server.id)
    SERVERS_LIST.append(server)

ROW = 0
COL = 0
# Write each Host and it's details in `Computers` tab
for server in SERVERS_LIST:
    COMPUTER.write(ROW, COL, "Hostname")
    COMPUTER.write(ROW + 1, COL, server.hostname)

    COMPUTER.write(ROW, COL + 1, "OS")
    COMPUTER.write(ROW + 1, COL + 1, server.os["name"])

    COMPUTER.write(ROW, COL + 2, "Groups")
    if server.groups:
        GROUPE_NAME = ""
        for group in server.groups:
            GROUPE_NAME += group.name + ", "
        GROUPE_NAME = GROUPE_NAME[:-1]
        COMPUTER.write(ROW + 1, COL + 2, GROUPE_NAME)

    COMPUTER.write(ROW, COL + 3, "Status")
    COMPUTER.write(ROW + 1, COL + 3, server.status["comment"])

    COMPUTER.write(ROW, COL + 4, "Criticality")
    COMPUTER.write(ROW + 1, COL + 4, server.criticality)

    COMPUTER.write(ROW, COL + 5, "Category")
    COMPUTER.write(ROW + 1, COL + 5, server.category)

    ROW += 3

ROW = 0
COL = 0
# Write vulnerabilities of each Host and it's details in `Vulnerabilities` tab
for server in SERVERS_LIST:
    VULNERABILITIES.write(ROW, COL, server.hostname)
    ROW += 1
    VULNERABILITIES.write(ROW, COL, "Vulnerabilty")
    VULNERABILITIES.write(ROW, COL + 1, "CVSS score v3")
    VULNERABILITIES.write(ROW, COL + 2, "CVSS score v2")
    VULNERABILITIES.write(ROW, COL + 3, "Exploitable")
    VULNERABILITIES.write(ROW, COL + 4, "Description")
    VULNERABILITIES.write(ROW, COL + 5, "Access vector v2")
    VULNERABILITIES.write(ROW, COL + 6, "Access complexity v2")
    VULNERABILITIES.write(ROW, COL + 7, "Authentication requirement v2")
    VULNERABILITIES.write(ROW, COL + 8, "Confidentiality impact v2")
    VULNERABILITIES.write(ROW, COL + 9, "Integrity impact v2")
    VULNERABILITIES.write(ROW, COL + 10, "Availability impact v2")
    VULNERABILITIES.write(ROW, COL + 11, "Access vector v3")
    VULNERABILITIES.write(ROW, COL + 12, "Access complexity v3")
    VULNERABILITIES.write(ROW, COL + 13, "Privilege requirement v3")
    VULNERABILITIES.write(ROW, COL + 14, "User Authentication v3")
    VULNERABILITIES.write(ROW, COL + 15, "Integrity impact v3")
    VULNERABILITIES.write(ROW, COL + 16, "Availability impact v3")
    VULNERABILITIES.write(ROW, COL + 17, "Confidentiality impact v3")
    VULNERABILITIES.write(ROW, COL + 18, "Scope v3")

    # Get details of each CVE
    for cve in server.cve_announcements:
        cve = CLIENT.cve_announcement(cve.cve_code)

        VULNERABILITIES.write(ROW + 1, COL, cve.cve_code)
        VULNERABILITIES.write(ROW + 1, COL + 1, cve.score_v3)
        VULNERABILITIES.write(ROW + 1, COL + 2, cve.score_v2)
        VULNERABILITIES.write(ROW + 1, COL + 3, cve.exploitable)
        VULNERABILITIES.write(ROW + 1, COL + 4, cve.content)

        if cve.cvss_v2 is not None:
            VULNERABILITIES.write(ROW + 1, COL + 5, cve.cvss_v2["access_vector"])
            VULNERABILITIES.write(ROW + 1, COL + 6, cve.cvss_v2["access_complexity"])
            VULNERABILITIES.write(ROW + 1, COL + 7, cve.cvss_v2["authentication"])
            VULNERABILITIES.write(ROW + 1, COL + 8, cve.cvss_v2["availability_impact"])
            VULNERABILITIES.write(ROW + 1, COL + 9, cve.cvss_v2["confidentiality_impact"])
            VULNERABILITIES.write(ROW + 1, COL + 10, cve.cvss_v2["integrity_impact"])

        if cve.cvss_v3 is not None:
            VULNERABILITIES.write(ROW + 1, COL + 11, cve.cvss_v3["access_vector"])
            VULNERABILITIES.write(ROW + 1, COL + 12, cve.cvss_v3["access_complexity"])
            VULNERABILITIES.write(ROW + 1, COL + 13, cve.cvss_v3["privilege_required"])
            VULNERABILITIES.write(ROW + 1, COL + 14, cve.cvss_v3["user_interaction"])
            VULNERABILITIES.write(ROW + 1, COL + 15, cve.cvss_v3["integrity_impact"])
            VULNERABILITIES.write(ROW + 1, COL + 16, cve.cvss_v3["availability_impact"])
            VULNERABILITIES.write(ROW + 1, COL + 17, cve.cvss_v3["confidentiality_impact"])
            VULNERABILITIES.write(ROW + 1, COL + 18, cve.cvss_v3["scope"])

        ROW += 1
    ROW += 2

ROW = 0
COL = 0
# Write each Host security announcements with details in `Security Advisories` tab
for server in SERVERS_LIST:
    SECURITY.write(ROW, COL, server.hostname)
    ROW += 1

    SECURITY.write(ROW, COL, "Security announcement code")
    SECURITY.write(ROW, COL + 1, "CVE Announcement")
    SECURITY.write(ROW, COL + 2, "Link")
    SECURITY.write(ROW, COL + 3, "Published date")
    SECURITY.write(ROW, COL + 4, "Updated date")

    for security_announcement in server.security_announcements:
        SECURITY.write(ROW + 1, COL, security_announcement["sa_code"])
        SECURITY.write(ROW + 1, COL + 2, security_announcement["link"])
        SECURITY.write(ROW + 1, COL + 3, security_announcement["created_at"])
        SECURITY.write(ROW + 1, COL + 4, security_announcement["updated_at"])

        for cve in security_announcement["cve_announcements"]:
            CVE_CODE_LIST += cve["cve_code"] + ", "
        CVE_CODE_LIST = CVE_CODE_LIST[:-1]
        SECURITY.write(ROW + 1, COL + 1, CVE_CODE_LIST)

        ROW += 1
    ROW += 2

ROW = 0
COL = 0
# Write each recommended actions/affected technologies of each Host in `Recommended Actions` tab
for server in SERVERS_LIST:
    RECOMMENDED.write(ROW, COL, server.hostname)
    ROW += 1

    RECOMMENDED.write(ROW, COL, "Affected technology")
    RECOMMENDED.write(ROW, COL + 1, "CVE announcement")
    RECOMMENDED.write(ROW, COL + 2, "Patchable")
    RECOMMENDED.write(ROW, COL + 3, "Current version")
    RECOMMENDED.write(ROW, COL + 4, "Target version")

    for update in server.updates:
        for cve in update["cve_announcements"]:
            CVE_CODE_LIST += cve["cve_code"] + ", "
        CVE_CODE_LIST = CVE_CODE_LIST[:-1]
        RECOMMENDED.write(ROW + 1, COL, update["current"]["product"])
        RECOMMENDED.write(ROW + 1, COL + 1, CVE_CODE_LIST)
        RECOMMENDED.write(ROW + 1, COL + 2, update["patchable"])
        RECOMMENDED.write(ROW + 1, COL + 3, update["current"]["version"])
        RECOMMENDED.write(ROW + 1, COL + 4, update["target"]["version"])

        ROW += 1
    ROW += 2

EXPORTED.close()
