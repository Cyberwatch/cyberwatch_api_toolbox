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
# For demo, limit to 5
SERVERS = SERVERS[:5]
print("INFO:Done.")

PRE_EXPORTED = """<html>
<head>
<style type="text/css">
table {
  color: #333;
  background: white;
  border: 1px solid grey;
  font-size: 12pt;
  border-collapse: collapse;
}
table thead th,
table tfoot th {
  color: #777;
  background: rgba(0,0,0,.1);
}
table caption {
  padding:.5em;
}
table th,
table td {
  padding: .5em;
  border: 1px solid lightgrey;
}
.critical {
  color: red;
  font-weight: bold;
}
table.cves tr th:first-child,
table.cves tr td:first-child {
  width: 130px;
  min-width: 130px;
  max-width: 130px;
  word-break: break-all;
}
</style>
</head>
<body width='595pt'>
"""

GLOBAL_COUNTERS = {"low": 0, "medium": 0, "high": 0, "critical": 0, "critical with exploit": 0}

# -----------------
# Report per computer
# -----------------
i = 0
EXPORTED = ""
for server in SERVERS:
    print("INFO:Generating " + str(server.hostname) + " part...")
    print("--- fetching details...")
    server = CLIENT.server(server.id)
    EXPORTED += "<h2>"+ str(server.hostname) +"</h2>"
    # -------------------
    # Write host summmary
    # -------------------
    print("--- generating characteristics...")
    EXPORTED += "<h3>Host characteristics</h3>"
    EXPORTED += "<table border=\"1\" >"
    EXPORTED += "<tr><th>" + "</th><th>".join("OS,Groups,Status,Criticality,Category".split(",")) + "</th></tr>"
    to_insert = "<tr>"
    # OS Name
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
    # Complete host characteristics
    EXPORTED += "</table>"
    # Summary of vulns
    print("--- generating summary of vulns...")
    counters = {"low": 0, "medium": 0, "high": 0, "critical": 0, "critical with exploit": 0}
    # Count cves based on their score
    for cve in server.cve_announcements:
        if cve.score is None:
            counters["low"] += 1
            GLOBAL_COUNTERS["low"] += 1
        elif cve.score > 9:
            counters["critical"] += 1
            GLOBAL_COUNTERS["critical"] += 1
            if cve.exploitable:
                counters["critical with exploit"] += 1
                GLOBAL_COUNTERS["critical with exploit"] += 1
        elif cve.score > 7:
            counters["high"] += 1
            GLOBAL_COUNTERS["high"] += 1
        elif cve.score > 5:
            counters["medium"] += 1
            GLOBAL_COUNTERS["medium"] += 1
        else:
            counters["low"] += 1
            GLOBAL_COUNTERS["low"] += 1
    EXPORTED += "<h3>Host vulnerabilities</h3>"
    EXPORTED += "<table border=\"1\" >"
    EXPORTED += "<tr><th>" + "</th><th>".join(
                "Critical with exploit,Critical,High,Medium,Low".split(",")) + "</th></tr>"
    EXPORTED += "<tr><td>"
    EXPORTED += "</td><td>".join([
        "<span class=\"critical\">"+str(counters["critical with exploit"])+"</span>",
        str(counters["critical"]),
        str(counters["high"]),
        str(counters["medium"]),
        str(counters["low"])
    ])
    EXPORTED += "</td></tr>"
    # Complete summary of vulns
    EXPORTED += "</table>"
    # Page break
    EXPORTED += "<div style = \"display:block; clear:both; page-break-after:always;\"></div>"

    # -----------------------
    # Vulnerabilities section
    # -----------------------
    print("--- generating details for vulnerabilities...")
    EXPORTED += "<h3>Vulnerabilities for "+str(server.hostname)+"</h3>"
    EXPORTED += "<table class=\"cves\" border=\"1\" >"
    EXPORTED += "<tr><th>" + "</th><th>".join("CVE code,CVSS score,Exploitable,Description".split(",")) + "</th></tr>"
    # Sort CVEs
    sorted_cves = sorted(server.cve_announcements, key=lambda x: x.score or 0, reverse=True)
    # Add details of each CVE
    for cve in sorted_cves:
        # Creating a line
        to_insert = "<tr>"
        # CVE_code
        to_insert += "<td>" + cve.cve_code + "</td>"
        # CVSS score
        score = 'N/A' if cve.score is None else str(cve.score)
        to_insert += "<td>" + score + "</td>"
        # Exploitability
        if cve.exploitable:
            to_insert += "<td class=\"critical\">" + str(cve.exploitable) + "</td>"
        else:
            to_insert += "<td>" + str(cve.exploitable) + "</td>"
        # Content
        content = 'N/A' if cve.content is None else cve.content
        to_insert += "<td>" + content + "</td>"
        # End of line
        to_insert += "</tr>"
        EXPORTED += to_insert
    # Complete vulns
    EXPORTED += "</table>"
    # Page break
    EXPORTED += "<div style = \"display:block; clear:both; page-break-after:always;\"></div>"

    # ---------------------------
    # Security advisories section
    # ---------------------------
    print("--- generating details for security advisories...")
    EXPORTED += "<h3>Security advisories for "+str(server.hostname)+"</h3>"
    EXPORTED += "<table border=\"1\" >"
    EXPORTED += "<tr><th>" + "</th><th>".join(
                "Security Advisory code, CVEs,Link,Published on,Updated on".split(",")) + "</th></tr>"
    # Add details of each SA
    for sa in server.security_announcements:
        # Creating a line
        to_insert = "<tr>"
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
    # Complete security advisories
    EXPORTED += "</table>"
    # Page break
    EXPORTED += "<div style = \"display:block; clear:both; page-break-after:always;\"></div>"

    # -------------------
    # Recommended actions
    # -------------------
    print("--- generating details for recommended actions...")
    EXPORTED += "<h3>Recommended actions for "+str(server.hostname)+"</h3>"
    EXPORTED += "<table border=\"1\" >"
    EXPORTED += "<tr><th>" + "</th><th>".join(
                "CVEs,Product,Current version,Target version".split(",")) + "</th></tr>"
    # Add details for recommended actions
    for update in server.updates:
        # Creating a line
        to_insert = "<tr>"
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
    # Complete recommended actions
    EXPORTED += "</table>"
    # Page break
    EXPORTED += "<div style = \"display:block; clear:both; page-break-after:always;\"></div>"

# -----------------
# Generate the HTML
# -----------------
# Generate the pre-report part
PRE_EXPORTED += "<h2>Example of report generated with Cyberwatch API</h2>"
PRE_EXPORTED += "<h3>Summary</h3>"
PRE_EXPORTED += "<table border=\"1\" >"
PRE_EXPORTED += "<tr><th>" + "</th><th>".join(
    "Assets,CVEs critical with exploit,CVEs critical,CVEs high,CVEs Medium,CVEs Low".split(",")
    ) + "</th></tr>"
PRE_EXPORTED += "<tr><td>"
PRE_EXPORTED += "</td><td>".join([
    str(len(SERVERS)),
    "<span class=\"critical\">"+str(GLOBAL_COUNTERS["critical with exploit"])+"</span>",
    str(GLOBAL_COUNTERS["critical"]),
    str(GLOBAL_COUNTERS["high"]),
    str(GLOBAL_COUNTERS["medium"]),
    str(GLOBAL_COUNTERS["low"])
])
PRE_EXPORTED += "</td></tr>"
# Complete summary of vulns
PRE_EXPORTED += "</table>"
PRE_EXPORTED += "<div style = \"display:block; clear:both; page-break-after:always;\"></div>"

# Add the footer
EXPORTED += """</body>
</html>"""

EXPORTED = PRE_EXPORTED + EXPORTED

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
