"""Generate a HTML email with the summary"""

import os
import smtplib
import ssl
from configparser import ConfigParser
from datetime import datetime
from email.mime.text import MIMEText
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(
    os.path.dirname(__file__)), '..', 'api.conf'))

############################################################
# CONFIGURATION - USE THIS SECTION TO CUSTOMIZE YOUR REPORTS
############################################################

# Filters to use, please comment unused parameters
# ( ["group"] or ["groupA", "groupB", "groupC"]...)
GROUPS = ["GROUPE_1","GROUP_2"]

# Add the following block to api.conf and set variables in SMTP_SETTINGS:
# [SMTP]
# server =
# login =
# password =

SMTP_SETTINGS = {
    "server": CONF.get('SMTP', 'server'),
    "port": 587,
    "username": CONF.get('SMTP', 'login'),
    "password": CONF.get('SMTP', 'password'),
    "sender": "",
    "recipient": ""
}

############################################################

print("! Testing communication with Cyberwatch API")
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get(
    'cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))
API_URL = CONF.get('cyberwatch', 'url')

CLIENT.ping()


def find_groups_details(GROUPS):
    '''d'''
    groups_id = []
    all_groups = CLIENT.groups()
    for group in GROUPS:
        for group_detail in all_groups:
            if group_detail.name == group:
                groups_id.append(group_detail.id)
    return groups_id


def get_servers_details():
    '''Find servers with group filters'''
    server_details = []
    for group_id in find_groups_details(GROUPS):
        filters = {"group_id": group_id}
        servers_with_groups = CLIENT.servers(filters)
        for server in servers_with_groups:
            server_details.append(CLIENT.server(str(server.id)))
    return server_details


def build_data():
    '''dd'''

    data_for_mail = []

    critical_cve_details_list = {}

    for server in get_servers_details():
        data = {
            'server_id':server.id,
            'hostname':server.hostname,
            'cve_count': 0,
            'critical_count': 0,
            'critical_with_exploit': 0,
            'critical_issues': 0,
            'major_issues': 0,
        }
        for cve in server.cve_announcements:
            data['cve_count'] += 1

            if cve.score is not None and cve.score >= 9:
                data['critical_count'] += 1
                if cve.cve_code not in critical_cve_details_list:
                    # faire un appel a l'api pour les details CVEs et stocker dans "critical_cve_details_list" pour eviter de dupliquer les appels
                    # ensuite calculer "critical_with_exploit"
                    critical_cve_details_list[cve.cve_code] = CLIENT.cve_announcement(str(cve.cve_code))
                    if critical_cve_details_list[cve.cve_code].exploitable :
                        data['critical_with_exploit'] += 1
                else:
                    # Si deja dans la liste, juste faire le calcul de "critical_with_exploit"
                    if critical_cve_details_list[cve.cve_code].exploitable :
                        data['critical_with_exploit'] += 1
                    print("")

        # Ensuite faire le calcul pour "critical_issues" et "major_issues" avant de build_email avec les donnees et envoyer le mail
        for security_issue in server.security_issues:
            if security_issue.level == "level_critical":
                data['critical_issues'] += 1
            if security_issue.level == "level_major":
                data['major_issues'] += 1
        
        data_for_mail.append(data)
    return data_for_mail


def build_email(cve_counts):
    '''Build HTML for email'''
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
<table bgcolor="#FFFFFF" cellpadding="0" cellspacing="0" class="nl-container" role="presentation" style="table-layout: fixed; vertical-align: top; min-width: 320px; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #FFFFFF; width: 100%;" valign="top" width="100%">
<tbody>

<tr style="vertical-align: top;" valign="top">
<td style="word-break: break-word; vertical-align: top;" valign="top">
<div style="background-color:transparent;">
<div class="block-grid" style="min-width: 320px; max-width: 500px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; Margin: 0 auto; background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;background-color:transparent;">
<div class="col num12" style="min-width: 320px; max-width: 500px; display: table-cell; vertical-align: top; width: 500px;">
<div class="col_cont" style="width:100% !important;">
<div style="border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:5px; padding-bottom:5px; padding-right: 0px; padding-left: 0px;">
<div style="color:#3e7bd6;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px;">
<div style="line-height: 1.2; font-size: 12px; color: #3e7bd6; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14px;">
<p style="font-size: 24px; line-height: 1.2; word-break: break-word; text-align: center; mso-line-height-alt: 29px; margin: 0;"><span style="font-size: 24px;"><strong>Veille sécurité Cyberwatch</strong></span></p>
</div>
</div>
<div style="color:#3c4858;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px;">
<div style="line-height: 1.2; font-size: 12px; color: #3c4858; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14px;">
<p style="font-size: 16px; line-height: 1.2; word-break: break-word; mso-line-height-alt: 19px; margin: 0;"><span style="font-size: 16px;"><strong>Liste des serveurs des groupes "{}" vulnérables :<br/></strong></span></p>
</div>
</div>
<div style="font-size:16px;text-align:center;font-family:Arial, Helvetica Neue, Helvetica, sans-serif">
<div style="text-align: center;"> <table class="tg" style="border-collapse:collapse;border-spacing:0;margin-left:auto;margin-right:auto;">
""".format(','.join(str(e) for e in GROUPS))

    html_end = """</table>
<div style="color:#555555;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px;">
<div style="line-height: 1.2; font-size: 12px; color: #555555; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14px;">
<p style="font-size: 14px; line-height: 1.2; word-break: break-word; mso-line-height-alt: 17px; margin: 0;">Message généré automatiquement par Cyberwatch.</p>
<p style="font-size: 14px; line-height: 1.2; word-break: break-word; mso-line-height-alt: 17px; margin: 0;">Toute notre équipe vous remercie pour votre confiance. Pour toute question, n'hésitez pas à contacter support@cyberwatch.fr</p>
</div>
</div>
</td>
</tr>
</tbody>
</table>
</body>
</html>
"""
    if cve_counts == {}:
        html = "<p>Aucun serveur avec une CVE critique, une CVE critique avec exploit ou un défaut de sécurité critique/majeur correspondant aux critères définis n'a été remonté</p>"
        data = html_start + html + html_end
        return data

    html_start += """
<thead>
<tr>
<th style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">Serveur</th>
<th style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">CVE</th>
<th style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">CVE critiques</th>
<th style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">CVE critiques avec exploit disponible</th>
<th style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">Défauts de sécurité critiques </th>
<th style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">Défauts de sécurité majeurs </th>

</tr>
</thead>
"""
    for line in cve_counts:
        html_for_each = """
<tr>
<td style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal"><a href="{}/servers/{}#server_cve_announcements"</a>{}</td>
<td style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">{}</td>
<td style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">{}</td>
<td style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">{}</td>
<td style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">{}</td>
<td style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">{}</td>
""".format(API_URL,line['server_id'],line['hostname'], line['cve_count'], line['critical_count'], line['critical_with_exploit'], line['critical_issues'], line['major_issues'])

        html_start += html_for_each

    html_start += html_end

    return html_start

cve_counts = build_data()
HTML = build_email(cve_counts)
print("! Testing communication with SMTP server")
context = ssl.create_default_context()
smtpserver = smtplib.SMTP(SMTP_SETTINGS["server"], SMTP_SETTINGS["port"])
smtpserver.ehlo() # Can be omitted
smtpserver.starttls(context=context) # Secure the connection
smtpserver.ehlo() # Can be omitted
smtpserver.login(SMTP_SETTINGS["username"], SMTP_SETTINGS["password"])
print("INFO:OK")

today = datetime.now().strftime("%Y-%m-%d %H:%M")
msg = MIMEText(HTML, 'html', 'utf-8')
msg['Subject'] = 'Cyberwatch - Bilan du '+ today
msg['From'] = SMTP_SETTINGS["sender"]
msg['To'] = SMTP_SETTINGS["recipient"]
smtpserver.send_message(msg)

smtpserver.quit()
