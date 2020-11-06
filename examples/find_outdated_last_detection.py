"""
Script to find servers with a last detection more than 40 days ago
Prerequisite :
- Set the constant variables on the first lines of the script
"""

import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

SENDER_EMAIL = ""
RECEIVER_EMAIL = ""

def connect_api():
    '''Connect to the API and test connection'''
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '..', 'api.conf'))
    client = CBWApi(conf.get('cyberwatch', 'url'), conf.get(
        'cyberwatch', 'api_key'), conf.get('cyberwatch', 'secret_key'))

    client.ping()
    return client


def analyse_cve_last_detection(server):
    '''Find servers with CVE last scanned more than 40 days ago'''
    for cve in server.cve_announcements:
        detected_at = datetime.strptime(cve.detected_at[:10], '%Y-%m-%d')
        now = datetime.now()
        delta = now - detected_at
        if delta.days > 40:
            return {"server": server, "last_detection": delta.days}
    return None


def find_outdated_cve(servers, client):
    '''Build list of servers with outdated `last detection`'''
    outdated_cve_servers = []
    for server in servers:
        server_details = client.server(str(server.id))
        outdated_scan = analyse_cve_last_detection(server_details)
        if outdated_scan:
            outdated_cve_servers.append(
                analyse_cve_last_detection(server_details))
    return outdated_cve_servers


def display(server_list, what):
    '''Display servers'''
    print('\n\n================= Total of {} servers {} ================='.format(
        len(server_list), what))
    for outdated_server in server_list:
        server = outdated_server["server"]
        print('{} --- {} --- {} --- Last Detection: {} days ago'.format(server.id, server.hostname,
        server.cve_announcements_count, outdated_server["last_detection"]))


def send_email(subject, sender, receiver, content, login, password, smtp, port):
    """Sends an email using smtp specified in the file api.conf"""
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content(content)

    server = smtplib.SMTP(smtp, port)
    server.starttls()
    server.login(login, password)
    server.send_message(msg)
    server.quit()

    print("\nSuccessfully sent email message to {}".format(receiver))


def build_email(server_list):
    """Send email with report"""
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '..', 'api.conf'))

    content = ''
    for outdated_server in server_list:
        server = outdated_server["server"]
        content += '\n{} --- {} --- {} --- Dernière Détection : {} jours'.format(server.id, server.hostname,
        server.cve_announcements_count, outdated_server["last_detection"])

    mail_content = """
    Bonjour,

    Cyberwatch a trouvé au total {} serveurs avec une dernière détection datant de plus de 40 jours :

    ID Serveur --- Hostname --- Nombre de CVEs --- Dernière Détection
    {}

    Cordialement,

    """.format(len(server_list), content)

    send_email(subject="Cyberwatch - Rapport 'dernière détection'", sender=SENDER_EMAIL,
               receiver=RECEIVER_EMAIL, login=conf.get('SMTP', 'login'),
               password=conf.get('SMTP', 'password'), content=mail_content, smtp=conf.get('SMTP', 'smtp'), port=587)


def launch_script():
    '''Launch script'''
    client = connect_api()
    servers = client.servers()
    outdated_cve = find_outdated_cve(servers, client)
    display(outdated_cve, 'with a CVE last detected more than 40 days ago')
    if outdated_cve:
        build_email(outdated_cve)


launch_script()
