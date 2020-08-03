"""Export active vulnerabilities published last month"""

import os
import datetime
from configparser import ConfigParser
import xlsxwriter
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

CLIENT.ping()

def get_cyberwatch_cves(start_date, end_date):
    """Returns a list of CVEs published between two dates"""
    parameters = {"active": "true"}
    exported_cves = []
    cves = CLIENT.cve_announcements(parameters)

    for cve in cves:
        if(cve.published is not None and parse_cyberwatch_date(cve.published) >= start_date
           and parse_cyberwatch_date(cve.published) < end_date):
            exported_cves.append(cve)

    print("{} unique CVEs affecting your computers were published between {} and {}."
          .format(len(exported_cves), start_date, end_date))
    return exported_cves

def parse_cyberwatch_date(cbwdate):
    """Convert a date retrieved from Cyberwatch API to a datetime object"""
    return datetime.datetime.strptime(cbwdate.split('T')[0], "%Y-%m-%d").date()

def get_updates(server):
    """Retrieves affected technology for a given CVE on a server object"""
    targeted_technology = ""
    targeted_version = ""

    for update in server.updates:
        if(update.target is not None and update.target.product is not None
           and update.target.version is not None):
            targeted_technology = update.target.product
            targeted_version = update.target.version
            break
    return targeted_technology, targeted_version

def instantiate_export(filename):
    """Instatiate the XLSX export"""
    xls_export = xlsxwriter.Workbook(filename)

    tab_unique_cve = xls_export.add_worksheet("Vulnerabilities by CVE code")
    tab_unique_cve.write(0, 0, "Vulnerability")
    tab_unique_cve.write(0, 1, "CVSS score v3")
    tab_unique_cve.write(0, 2, "CVSS score v2")
    tab_unique_cve.write(0, 3, "Exploit code maturity")
    tab_unique_cve.write(0, 4, "Number of affected computers")
    tab_unique_cve.write(0, 5, "Number of fixed computers")
    tab_unique_cve.write(0, 6, "Publication date")

    tab_computer_cve = xls_export.add_worksheet("Vulnerabilities by computer")
    tab_computer_cve.write(0, 0, "Vulnerability")
    tab_computer_cve.write(0, 1, "CVSS score v3")
    tab_computer_cve.write(0, 2, "CVSS score v2")
    tab_computer_cve.write(0, 3, "Exploit code maturity")
    tab_computer_cve.write(0, 4, "Affected computer")
    tab_computer_cve.write(0, 5, "Concerned technologies")
    tab_computer_cve.write(0, 6, "Targeted version")
    tab_computer_cve.write(0, 7, "Publication date")

    return xls_export

def export_xls(cve_list, xls_export):
    """Export a list of CVEs to an XLS file"""
    row_unique_cve = 1
    row_computer_cve = 1
    cve_len = len(cve_list)

    tab_unique_cve = xls_export.get_worksheet_by_name("Vulnerabilities by CVE code")
    tab_computer_cve = xls_export.get_worksheet_by_name("Vulnerabilities by computer")

    try:
        for cve in cve_list:
            cve = CLIENT.cve_announcement(cve.cve_code)
            print("Progress : {}/{} -- {}".format(row_unique_cve, cve_len, cve.cve_code), end="\r")

            count_affected_computers = 0
            count_fixed_computers = 0

            for server in cve.servers:
                # Skip if the CVE is not active on the server
                if server.active is not True:
                    count_fixed_computers += 1
                    continue
                count_affected_computers += 1
                targeted_technology, targeted_version = get_updates(server)

                tab_computer_cve.write(row_computer_cve, 0, cve.cve_code)
                tab_computer_cve.write(row_computer_cve, 1, cve.score_v3)
                tab_computer_cve.write(row_computer_cve, 2, cve.score_v2)
                tab_computer_cve.write(row_computer_cve, 3, cve.exploit_code_maturity)
                tab_computer_cve.write(row_computer_cve, 4, server.hostname)
                tab_computer_cve.write(row_computer_cve, 5, targeted_technology)
                tab_computer_cve.write(row_computer_cve, 6, targeted_version)
                tab_computer_cve.write(row_computer_cve, 7, cve.published)
                row_computer_cve += 1

            tab_unique_cve.write(row_unique_cve, 0, cve.cve_code)
            tab_unique_cve.write(row_unique_cve, 1, cve.score_v3)
            tab_unique_cve.write(row_unique_cve, 2, cve.score_v2)
            tab_unique_cve.write(row_unique_cve, 3, cve.exploit_code_maturity)
            tab_unique_cve.write(row_unique_cve, 4, count_affected_computers)
            tab_unique_cve.write(row_unique_cve, 5, count_fixed_computers)
            tab_unique_cve.write(row_unique_cve, 6, cve.published)
            row_unique_cve += 1
    except:
        print("An error has occured")
        print("Only {} out of {} vulnerabilities were successfully exported".format(row_unique_cve+1, cve_len))
        raise
    finally:
        xls_export.close()

# Defines date to retrieve CVEs published last month
today = datetime.date.today()
firstDayOfLastMonth = (today.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
firstDayOfCurrentMonth = today.replace(day=1)

print("Exporting vulnerabilities published between {} and {}.".format(firstDayOfLastMonth, firstDayOfCurrentMonth))
export_xls(get_cyberwatch_cves(firstDayOfLastMonth, firstDayOfCurrentMonth),
           instantiate_export("active_CVEs_{}_to_{}_export.xlsx".format(firstDayOfLastMonth, firstDayOfCurrentMonth)))
