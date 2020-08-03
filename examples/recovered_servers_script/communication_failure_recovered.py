"""Create a file with servers in "Communication Failure" and find recovered servers"""""

import argparse
import os
import json
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, date
from configparser import ConfigParser
from cbw_api_toolbox.cbw_api import CBWApi

EMAIL_RECEIVERS = ["", ""]


def connect_api():
    """Connect to the API and test connection"""
    print("INFO: Checking API connection and credentials...")
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '.', 'api.conf'))
    client = CBWApi(conf.get('cyberwatch', 'url'), conf.get(
        'cyberwatch', 'api_key'), conf.get('cyberwatch', 'secret_key'))

    client.ping()
    return client


def setup_smtp():
    """Setup variables for SMTP"""
    print("INFO: Setting up SMTP variables...")
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '.', 'smtp.conf'))
    smtp = {
        "server": conf.get('smtp', 'smtp_server'),
        "login": conf.get('smtp', 'smtp_login'),
        "password": conf.get('smtp', 'smtp_password'),
        "port": conf.get('smtp', 'smtp_port'),
        "sender": conf.get('smtp', 'smtp_sender'),
    }
    return smtp


def replace_file(servers):
    """Replace server list in file with recent one"""
    print("INFO: Replacing server list in file with recent one...")
    if os.path.exists(os.path.dirname(__file__) + '/communication_failure_list.txt'):
        try:
            os.remove(os.path.dirname(__file__) +
                      '/communication_failure_list.txt')
        except OSError as error:
            print("Error: %s - %s." % (error.filename, error.strerror))
    find_communication_failure_servers(servers)


def find_communication_failure_servers(servers):
    """Find servers with status "Communication failure" and save them to a file"""
    print('INFO: Finding servers with "Communication failure" status and saving result in file')
    with open(os.path.dirname(__file__) + '/communication_failure_list.txt', 'w+') as file:
        for server in servers:
            if server.status == "server_update_comm_fail":
                json.dump({"id": server.id}, file)
                file.write(os.linesep)


def find_recovered_servers(client):
    """Compare list of servers in file with current ones to find recovered servers"""
    print("INFO: Determining recovered servers by comparing current servers with list in file...")
    current_servers_list = []
    for server in client.servers():
        if server.status == "server_update_comm_fail":
            current_servers_list.append({"id": server.id})

    with open(os.path.dirname(__file__) + '/communication_failure_list.txt') as file:
        server_list = [json.loads(line) for line in file]

    diff = [i for i in current_servers_list +
            server_list if i not in current_servers_list or i not in server_list]

    return diff


def build_server_list(client, diff):
    """Fetch each server that recovered to help build the email report"""
    print("INFO: Fetching each server not in 'Communication failure' anymore...")
    servers = []
    for server in diff:
        servers.append(client.server(str(server.id)))
    return servers


def create_body_html(client, server_list):
    """Make an HTML list from server list for email"""
    servers_html = ""
    for server in server_list:
        link = '<a href="{}/servers/{}">{}</a>'.format(
            client.api_url, server.id, server.hostname)
        html = """{}<br />""".format(link)
        servers_html += html

    return servers_html


def send_email(client, smtp, server_list):
    """Sends an email using smtp configuration specified in the file smtp.conf"""
    content = create_body_html(client, server_list)

    # Email Configuration
    message = MIMEMultipart("alternative")
    message["Subject"] = '[Cyberwatch] Servers recovered from "Communication failure" report - ' + \
        date.today().strftime("%m/%d/%y")
    message["From"] = smtp["sender"]
    message["To"] = ", ".join(EMAIL_RECEIVERS)

    # Get Period start date with "Last Modified" time of file
    start_date = datetime.fromtimestamp(os.path.getmtime(os.path.dirname(
        __file__) + '/communication_failure_list.txt')).strftime("%d/%m/%Y, %H:%M")

    email_body = f"""\
    <p>Greetings,</p>

    <p>Please find in the following section, a list of servers that recovered from the status
    "Communication failure".</p>

    <span style="color:#4bb9f1;font-size:18px;align:center"><strong>Servers recovered from "Communication Failure"
     between {start_date} and {datetime.now().strftime("%d/%m/%Y, %H:%M")}</strong></span>
    <br />

    <br />{content}<br />

    <p>The Cyberwatch Team - support@cyberwatch.fr</p>
    """

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(MIMEText(email_body, "plain"))
    message.attach(MIMEText(email_body, "html"))

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp["server"], smtp["port"], context=context) as server:
        server.login(smtp["login"], smtp["password"])
        server.sendmail(
            smtp["sender"], EMAIL_RECEIVERS, message.as_string()
        )

    print("Successfully sent email  to {}".format(message["To"]))


def launch_script():
    '''Launch script'''
    client = connect_api()
    smtp = setup_smtp()
    print("INFO: Getting server list...")
    servers = client.servers()
    if os.path.exists(os.path.dirname(__file__) + '/communication_failure_list.txt') is False:
        find_communication_failure_servers(servers)
    diff = find_recovered_servers(client)
    server_list = build_server_list(client, diff)
    send_email(client, smtp, server_list)
    replace_file(servers)


def main(args=None):
    '''Main function'''

    parser = argparse.ArgumentParser(
        description="""Script using Cyberwatch API to find servers recovered from the status 'Communication failure'""")

    parser.parse_args(args)
    launch_script()


if __name__ == '__main__':
    main()
