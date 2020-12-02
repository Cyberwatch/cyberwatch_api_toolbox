"""Example script sending an email report on vulnerabilities with exploit"""

import smtplib
import os
from email.message import EmailMessage
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))

def send_email(subject, sender, receiver, content, login, password, smtp, port):
    """Sends an email using smtp specified in the file api.conf"""
    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = sender
    email['To'] = receiver
    email.set_content(content)

    server = smtplib.SMTP(smtp, port)
    server.starttls()
    server.login(login, password)
    server.send_message(email)
    server.quit()

    print("Successfully sent email message to {}".format(receiver))

def retrieve_api_informations():
    """Returns a report on vulnerabilities from Cyberwatch's API"""
    client = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'),\
             CONF.get('cyberwatch', 'secret_key'))
    client.ping()

    all_cves_filter = {"active": "true"}
    all_cves = client.cve_announcements(all_cves_filter)

    critical_with_exploit_filter = {"exploit_code_maturity": ["proof_of_concept"],
                                    "active": "true", "level": "level_critical"}
    critical_cves = client.cve_announcements(critical_with_exploit_filter)

    high_with_exploit_filter = {"exploit_code_maturity": ["high"], "active": "true", "level": "level_high"}
    high_cves = client.cve_announcements(high_with_exploit_filter)

    mail_content = """
    Bonjour,
    
    Cyberwatch a détecté {} vulnérabilités dont :
    - {} vulnérabilités critiques (score ≥ 9) avec exploit public \
    (Voir {}/cve_announcements?severity[]=level_critical&present=true&exploit_code_maturity[]=high\
    &exploit_code_maturity[]=functional&exploit_code_maturity[]=proof_of_concept&sort_by=published&order=asc)
    - {} vulnérabilités élevées (9 > score ≥ 7) avec exploit public \
    (Voir {}/cve_announcements?severity[]=level_high&present=true&exploit_code_maturity[]=high\
    &exploit_code_maturity[]=functional&exploit_code_maturity[]=proof_of_concept&sort_by=published&order=asc)."""\
    .format(len(all_cves), len(critical_cves), CONF.get('cyberwatch', 'url'), \
    len(high_cves), CONF.get('cyberwatch', 'url'))

    return mail_content

send_email(subject="Rapport Cyberwatch", sender="sender@xxx.fr", receiver="receiver@xxx.fr", \
           login=CONF.get('SMTP', 'login'), password=CONF.get('SMTP', 'password'), \
           content=retrieve_api_informations(), smtp=CONF.get('SMTP', 'smtp'), port=587)
