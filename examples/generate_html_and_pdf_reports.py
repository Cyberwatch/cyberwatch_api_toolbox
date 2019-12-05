"""Example: generate HTML and PDF reports"""

import os
from configparser import ConfigParser
import pdfkit # pylint: disable=import-error
from cbw_api_toolbox.cbw_api import CBWApi

# Requires wkhtmltopdf
# See https://github.com/JazzCore/python-pdfkit for details

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

print("INFO:Checking access...")
CLIENT.ping()

print("INFO:Fetching assets list...")
SERVERS = CLIENT.servers()
print("INFO:Done.")

EXPORTED = """<html>
<head></head>
<body width='595pt'>
"""

EXPORTED += """</body>
</html>"""

# Build a list with each server and it's details
print("INFO:Fetching assets details...")
SERVERS_LIST = []
for server in SERVERS:
    server = CLIENT.server(server.id)
    SERVERS_LIST.append(server)
print("INFO:Done.")

# -----------------
# Computers section
# -----------------
print("INFO:Generating Computers part...")
EXPORTED += "<h2>Computers</h2>"
EXPORTED += "<table border=\"1\" >"
EXPORTED += "<tr><th>" + "</th><th>".join("Hostname,OS,Groups,Status,Criticality,Category".split(",")) + "</th></tr>"
# Write each Host and its details
for server in SERVERS_LIST:
    to_insert = "<tr>"
    # Hostname
    to_insert += "<td>" + server.hostname + "</td>"
    # Name
    to_insert += "<td>" + server.os["name"] + "</td>"
    # Groups
    to_insert_groups = ""
    if server.groups:
        group_name = ""
        for group in server.groups:
            group_name += group.name + ", "
        to_insert_groups = group_name[:-2]
    to_insert += "<td>" + to_insert_groups + "</td>"
    # Status
    to_insert += "<td>" + server.status["comment"] + "</td>"
    # Criticality
    to_insert += "<td>" + server.criticality + "</td>"
    # Category
    to_insert += "<td>" + server.category + "</td>"
    to_insert += "</tr>"
    EXPORTED += to_insert
EXPORTED += "</table>"
print("INFO:Done.")

EXPORTED += "<div style = \"display:block; clear:both; page-break-after:always;\"></div>"

# -----------------------
# Vulnerabilities section
# -----------------------
print("INFO:Generating Vulnerabilities part...")
EXPORTED += "<h2>Vulnerabilities</h2>"
EXPORTED += "<table border=\"1\" >"
EXPORTED += "<tr><th>" + "</th><th>".join(
    "Hostname,CVE code,CVSS score,Exploitable,Description".split(",")) + "</th></tr>"
# Write vulnerabilities of each Host with details
for server in SERVERS_LIST:
    print("----- generating vulnerabilities for " + server.hostname + "...")
    # Add details of each CVE
    for cve in server.cve_announcements:
        # Creating a line
        to_insert = "<tr>"
        # Hostname
        to_insert += "<td>" + server.hostname + "</td>"
        # CVE_code
        to_insert += "<td>" + cve.cve_code + "</td>"
        # CVSS score
        score = 'N/A' if cve.score is None else str(cve.score)
        to_insert += "<td>" + score + "</td>"
        # Exploitability
        to_insert += "<td>" + str(cve.exploitable) + "</td>"
        # Content
        content = 'N/A' if cve.content is None else cve.content
        to_insert += "<td>" + content + "</td>"
        # End of line
        to_insert += "</tr>"
        EXPORTED += to_insert
EXPORTED += "</table>"
print("INFO:Done.")

EXPORTED += "<div style = \"display:block; clear:both; page-break-after:always;\"></div>"

# ---------------------------
# Security advisories section
# ---------------------------
print("INFO:Generating Security advisories part...")
EXPORTED += "<h2>Security advisories</h2>"
EXPORTED += "<table border=\"1\" >"
EXPORTED += "<tr><th>" + "</th><th>".join(
    "Hostname,Security Advisory code, CVEs,Link,Published on,Updated on".split(",")) + "</th></tr>"
# Write security advisories of each Host with details
for server in SERVERS_LIST:
    print("----- generating security advisories for " + server.hostname + "...")
    # Add details of each SA
    for sa in server.security_announcements:
        # Creating a line
        to_insert = "<tr>"
        # Hostname
        to_insert += "<td>" + server.hostname + "</td>"
        # SA code
        to_insert += "<td>" + sa["sa_code"] + "</td>"
        # CVE codes
        cves_to_add = ""
        for cve in sa["cve_announcements"]:
            cves_to_add += cve["cve_code"] + ", "
        cves_to_add = cves_to_add[:-2]
        to_insert += "<td>" + cves_to_add + "</td>"
        # Link
        to_insert += '<td><a href="' + sa["link"] + '">' + sa["link"] + '</a></td>'
        # Published on
        to_insert += "<td>" + sa["created_at"].split('T')[0] + "</td>"
        # Updated on
        to_insert += "<td>" + sa["updated_at"].split('T')[0] + "</td>"
        # End of line
        to_insert += "</tr>"
        EXPORTED += to_insert
EXPORTED += "</table>"
print("INFO:Done.")

EXPORTED += "<div style = \"display:block; clear:both; page-break-after:always;\"></div>"

# -------------------
# Recommended actions
# -------------------
print("INFO:Generating Recommended actions part...")
EXPORTED += "<h2>Recommended actions</h2>"
EXPORTED += "<table border=\"1\" >"
EXPORTED += "<tr><th>" + "</th><th>".join(
    "Hostname,CVEs,Product,Current version,Target version".split(",")) + "</th></tr>"
## Write each recommended actions/affected technologies of each Host with details
for server in SERVERS_LIST:
    print("----- generating recommended actions for " + server.hostname + "...")
    for update in server.updates:
        # Creating a line
        to_insert = "<tr>"
        # Hostname
        to_insert += "<td>" + server.hostname + "</td>"
        # CVE codes
        cves_to_add = ""
        for cve in update["cve_announcements"]:
            cves_to_add += cve["cve_code"] + ", "
        cves_to_add = cves_to_add[:-2]
        to_insert += "<td>" + cves_to_add + "</td>"
        # Product
        to_insert += "<td>" + update["current"]["product"] + "</td>"
        # Current version
        to_insert += "<td>" + update["current"]["version"] + "</td>"
        # Target version
        to_insert += "<td>" + update["target"]["version"] + "</td>"
        # End of line
        to_insert += "</tr>"
        EXPORTED += to_insert
EXPORTED += "</table>"
print("INFO:Done.")

# -----------------
# Generate the HTML
# -----------------

print("INFO:Generating HTML...")
FILEOUT = open("report.html", "w")
FILEOUT.writelines(EXPORTED)
FILEOUT.close()
print("INFO:Done.")

# ----------------
# Generate the PDF
# ----------------

print("INFO:Generating PDF...")
pdfkit.from_file('report.html', 'report.pdf')
print("INFO:Done.")
print("INFO:End of script.")
