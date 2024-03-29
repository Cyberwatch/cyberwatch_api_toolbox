"""Find latest high-priority CVEs and send a report"""

import os
import glob
import smtplib
import json
import ssl
from email.mime.text import MIMEText
from configparser import ConfigParser
from datetime import datetime, timedelta
from cbw_api_toolbox.cbw_api import CBWApi

############################################################
# CONFIGURATION - USE THIS SECTION TO CONFIGURE SCRIPT
############################################################

# Add the following block to api.conf and set variables in smtp_settings:
# [SMTP]
# server =
# login =
# password =

SENDER_EMAIL = ""
RECEIVER_EMAILS = ""
SUBJECT = "Cyberwatch - Rapport 'CVEs prioritaires'"


def connect_api():
    '''Connect to the API and test connection'''
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '..', '..', 'api.conf'))
    client = CBWApi(conf.get('cyberwatch', 'url'), conf.get(
        'cyberwatch', 'api_key'), conf.get('cyberwatch', 'secret_key'))
    client.ping()
    return client


def compare_for_new_cve(new_set):
    '''Find new high-priority CVEs by comparing with last backup and write a new backup'''
    old_high_priority_cves = {}

    # Get latest backup of high-priority CVEs
    list_of_files = glob.glob((os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '*new_cves.json')))
    old_backup = open(max(list_of_files, key=os.path.getctime), "r")
    old_list = json.load(old_backup)
    old_backup.close()

    # Compare old backup with latest high-priority CVEs
    new_unique_high_priority_list = {k: v for k,
                                     v in new_set.items() if k not in old_list}

    # Write new backup file with all high-priority CVEs
    new_backup = open((os.path.join(os.path.abspath(
        os.path.dirname(__file__)), datetime.strftime(datetime.now(), '%d-%m-%Y') + "_new_cves.json")), "w")
    new_backup.write(json.dumps({**old_high_priority_cves, **new_set}))
    new_backup.close()

    return new_unique_high_priority_list


def find_new_high_priority_cve_set(servers, client):
    '''Find latest high-priority CVEs'''
    new_high_priority_cve_set = {}
    for server in servers:
        server_details = client.server(str(server.id))
        for cve in server_details.cve_announcements:
            if cve.prioritized:
                new_high_priority_cve_set[cve.cve_code] = cve.score
    return new_high_priority_cve_set


def display(cve_list, what):
    '''Display result'''
    print('\n\n================= Total of {} {} ================='.format(
        len(cve_list), what))
    for key, value in cve_list.items():
        print(key, value)


def send_email(html):
    """Sends an email using smtp specified in the file api.conf"""

    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '..', '..', 'api.conf'))

    smtp_settings = {
        "server": conf.get('SMTP', 'smtp'),
        "port": 587,
        "username": conf.get('SMTP', 'login'),
        "password": conf.get('SMTP', 'password'),
        "sender": SENDER_EMAIL,
        "recipient":  RECEIVER_EMAILS
    }

    print("! Testing communication with SMTP server")
    context = ssl.create_default_context()
    smtpserver = smtplib.SMTP(smtp_settings["server"], smtp_settings["port"])
    smtpserver.starttls(context=context)  # Secure the connection
    smtpserver.login(smtp_settings["username"], smtp_settings["password"])
    print("INFO:OK")

    today = datetime.now().strftime("%d-%m-%Y")
    msg = MIMEText(html, 'html', 'utf-8')
    msg['Subject'] = SUBJECT + " - " + today
    msg['From'] = smtp_settings["sender"]
    msg['To'] = smtp_settings["recipient"]
    smtpserver.send_message(msg)

    smtpserver.quit()


def build_email(cve_list):
    """Send email with report"""
    conf = ConfigParser()
    conf.read(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '..', '..', 'api.conf'))
    api_url = conf.get('cyberwatch', 'url')
    yesterday = datetime.today() - timedelta(days=1)

    html_start = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">
    <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
    <meta content="width=device-width" name="viewport"/>
    <meta content="IE=edge" http-equiv="X-UA-Compatible"/>
    <title></title>
    </head>
    <body class="clean-body" style="margin: 0; padding: 0; -webkit-text-size-adjust: 100%; background-color: #FFFFFF;">
    <table bgcolor="#FFFFFF" cellpadding="0" cellspacing="0" class="nl-container" role="presentation" style="table-layout: fixed; vertical-align: top; min-width: 320px; border-spacing: 0; border-collapse: collapse;background-color: #FFFFFF; width: 100%;" valign="top" width="100%">
    <tbody>
    <td valign="top" align="center">
    <div style="background-color: rgb(255, 255, 255); border-radius: 0px;">
    <table class="rnb-del-min-width" style="min-width:590px;" name="Layout_1" id="Layout_1" width="100%" cellspacing="0" cellpadding="0" border="0">
    <tbody>
    <tr>
    <td class="rnb-del-min-width" style="min-width:590px;" valign="top" align="center">
    <a href="#" name="Layout_1"></a>
    <table class="rnb-container" style="background-image: url(https://img.mailinblue.com/2711508/images/rnb/original/5ebec9f1f903a0bf0a1403ed.jpeg); background-position: center top; background-size: auto; background-repeat: no-repeat; background-color: rgb(255, 255, 255); border-radius: 0px; padding-left: 20px; padding-right: 20px; border-collapse: separate;" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff">
    <tbody>
    <tr>
    <td style="font-size:1px; line-height:20px;" height="20">&nbsp;</td>
    </tr>
    <tr>
    <td class="rnb-container-padding" valign="top" align="left">
    <table width="100%" cellspacing="0" cellpadding="0" border="0" align="center">
    <tbody>
    <tr>
    <td valign="top" align="center">
    <table class="logo-img-center" cellspacing="0" cellpadding="0" border="0" align="center">
    <tbody>
    <tr>
    <td style="line-height: 1px;" valign="middle" align="center">
    <div style="border-top:0px None #9c9c9c;border-right:0px None #9c9c9c;border-bottom:0px None #9c9c9c;border-left:0px None #9c9c9c;display:inline-block; " cellspacing="0" cellpadding="0" border="0">
    <div><img alt="Cyberwatch" style="float: left;max-width:116px;display:block;" class="rnb-logo-img" src="https://img-cache.net/im/2711508/a42c6297eebabaa5fadd15aff5fb35fe288fc0f536769c764a89ed11452be8a3.png?e=bIddPVwUeVGJCR_ByqupQeKjwH1b4wWpc7zMt5ina_Cck1ujDSDW6lRRr_SK-oN99efOWYXRJSg54p8dVcM-f_kcfB8wVu5-tawI2yj9upVF-zm2DaWasPK69uaZ0TVlNiQPzkpv84u4PR-YJkqrS7qhj4oCx7Azjp5MFGpSZ5XnEKSU_S1KU8VEO9_SbXPLg_dTid3sfk9ib6bSv6m_ezKg8e9z_1nzxS4utZw3ZcturC1F-pGsRNB9-9sMB5FNmYv1J_tsnldi6w" width="116" vspace="0" hspace="0" border="0"></div>
    </div>
    </td>
    </tr>
    </tbody>
    </table>
    </td>
    </tr>
    </tbody>
    </table>
    </td>
    </tr>
    <tr>
    <td style="font-size:1px; line-height:20px;" height="20">&nbsp;</td>
    </tr>
    </tbody>
    </table>
    <tr style="vertical-align: top;" valign="top">
    <td style="word-break: break-word; vertical-align: top;" valign="top">
    <div style="background-color:transparent;">
    <div class="block-grid" style="min-width: 320px; max-width: 500px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; Margin: 0 auto; background-color: transparent;">
    <div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
    <div class="col num12" style="min-width: 320px; max-width: 500px; display: table-cell; vertical-align: top; width: 500px;">
    <div class="col_cont" style="width:100% !important;">
    <div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:5px; padding-bottom:5px; padding-right: 0px; padding-left: 0px;">
    <div style="color:#3e7bd6;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px;">
    <div style="line-height: 1.2; font-size: 12px; color: #3e7bd6; font-family: Arial, Helvetica Neue, Helvetica, sans-serif;">
    <p style="font-size: 24px; line-height: 1.2; word-break: break-word; text-align: center; margin: 0;"><span style="font-size: 24px;"><strong>Veille sécurité Cyberwatch</strong></span></p>
    </div>
    </div>
    <div style="font-size:16px;text-align:center;font-family:Arial, Helvetica Neue, Helvetica, sans-serif">
    <div style="text-align: center;"> <table class="tg" style="border-collapse:collapse;border-spacing:0;margin-left:auto;margin-right:auto;">
    """

    html_end = """
    </ul>
    </td>
    </div>
    </div>
    </div>
    </table>
    <div style="color:#555555;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px;border-top: 3px solid #bbb;">
    <div style="line-height: 1.2; font-size: 12px; color: #555555; font-family: Arial, Helvetica Neue, Helvetica, sans-serif;">
    <p style="font-size: 14px; line-height: 1.2; margin: 0;">Message généré automatiquement par Cyberwatch.</p>
    <p style="font-size: 14px; line-height: 1.2; margin: 0;">Toute notre équipe vous remercie pour votre confiance. Pour toute question, n'hésitez pas à contacter support@cyberwatch.fr</p>
    </table>
    </body>
    </html>"""

    if len(cve_list) == 0:
        html = """<p>Aucune nouvelle CVE prioritaire détectée depuis {}</p>""".format(
            datetime.strftime(yesterday, '%d-%m-%Y'))
        final_html = html_start + html + html_end

    else:
        html_start += """
        <div style="color:#3c4858;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px;">
        <div style="line-height: 1.2; font-size: 12px; color: #3c4858; font-family: Arial, Helvetica Neue, Helvetica, sans-serif;>
        <p style="font-size: 16px; line-height: 1.2; word-break: break-word; margin: 0;"><span style="font-size: 16px;"><strong>Listes des nouvelles CVEs prioritaires depuis le {} :<br/></strong></span></p>
        <ul style="font-family:Arial;font-size:15px;list-style:none;text-align: start;">
        """.format(datetime.strftime(yesterday, '%d-%m-%Y'))

        for cve in cve_list.items():
            html_for_each = """
            <li>
            <a href="{}/cve_announcements/{}">{}</a> (score <span><strong>{}</strong>)</span>
            </li>
            """.format(
                api_url, cve[0], cve[0], cve[1])
            html_start += html_for_each
        final_html = html_start + html_end

    return final_html


def launch_script():
    '''Launch script'''
    client = connect_api()
    servers = client.servers()
    latest_high_priority_cve_set = find_new_high_priority_cve_set(
        servers, client)
    cve_list = compare_for_new_cve(latest_high_priority_cve_set)
    display(cve_list, 'new high-priority CVEs')
    html = build_email(cve_list)
    send_email(html)


launch_script()
