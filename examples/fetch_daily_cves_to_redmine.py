"""Integration script with redmine ; the script :
- fetch all CVEs present in Cyberwatch
- compares the list fetched today with CVEs fetched yesterday
- send a Redmine API request to create an issue for each new CVE"""

import os
import sys
from configparser import ConfigParser
from datetime import datetime, timedelta
#pip3 install python-redmine : https://python-redmine.com/installation.html
from redminelib import Redmine # pylint: disable=import-error
from cbw_api_toolbox.cbw_api import CBWApi

def send_redmine(cve_list, project_id, tracker_id):
    """Takes a list of CVEs and create an issue in Redmine for each, with affected servers"""
    for cve_code in cve_list:
        message = """Une nouvelle vulnérabilité a été détectée : {}
Celle-ci affecte les actifs suivants :"""\
        .format("\""+cve_code+"\":"+CONF.get('cyberwatch', 'url')+"/cve_announcements/"+cve_code)
        cve = CLIENT.cve_announcement(cve_code)
        for server in cve.servers:
            message += "\n\n* \""+server.hostname+"\":"+CONF.get('cyberwatch', 'url')+"/servers/"+str(server.id)

        if cve.level is not None:
            redmine_priority_id = redmine_priorities[cve.level[6:]]
        else:
            redmine_priority_id = redmine_priorities["unknown"]

        with redmine.session(return_response=False):
            redmine.issue.create(project_id=project_id, subject='Cyberwatch new CVE : {}'.format(cve.cve_code), \
            priority_id=redmine_priority_id, description=message, tracker_id=tracker_id)

def get_cves_today():
    """Get list of CVEs present in Cyberwatch and create a file"""

    # Fetching CVEs present date of today
    print("! Fetching CVEs present today...")
    parameters = {"active": "true"}
    cves = CLIENT.cve_announcements(parameters)
    print("* "+str(cves.__len__())+" CVEs found for today, sorting and priting them...")

    cve_list_today = []
    for cve in cves:
        cve_list_today.append(cve.cve_code)
    cve_list_today.sort()

    today_date = datetime.strftime(datetime.now(), '%Y-%m-%d')

    print("* Saving the results to data/"+today_date+".txt")
    with open("data/"+today_date+".txt", "w") as outfile:
        outfile.write("\n".join(cve_list_today))
    print("! Done.")

    return cve_list_today

def get_cves_yesterday():
    """Use CVEs saved in the file created yesterday"""
    # Getting CVEs present in the file saved yesterday
    print("! Reading CVEs present yesterday...")
    yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    print("* Yesterday: " + yesterday_date)

    cve_list_yesterday = []
    with open("data/"+yesterday_date+".txt") as infile:
        for line in infile:
            cve_list_yesterday.append(line.strip())

    print("* "+str(cve_list_yesterday.__len__())+" CVEs found yesterday...")
    print("! Done.")

    return cve_list_yesterday

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
# Cyberwatch API informations
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))
CLIENT.ping()

# Redmine API informations
redmine = Redmine(CONF.get('redmine', 'url'), version=CONF.get('redmine', 'version'), key=CONF.get('redmine', 'key'))
# id of the Redmine project to affect newly created issues to
REDMINE_PROJECT_ID = 2
# id of the tracker ; optional if a default tracker is defined in Redmine
REDMINE_TRACKER_ID = 1
# dict of priorities and their ids in Redmine, available through admin interface : http://[redmine-url]/enumerations
redmine_priorities = {
    "low": 5,
    "medium": 4,
    "high": 3,
    "critical": 2,
    "unknown": 7
}

# Finding the differences between yesterday and today
print("! Computing the difference...")
diff = list(set(get_cves_today()) - set(get_cves_yesterday()))
diff.sort()
print(diff)

if len(diff) == 0:
    print("No new CVEs found between yesterday and today: nothing to send!")
    sys.exit(0)

send_redmine(diff, REDMINE_PROJECT_ID, REDMINE_TRACKER_ID)
