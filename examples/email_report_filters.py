"""Generate a HTML email with the summary of new CVEs detected / modified since a specific date"""

import os
import smtplib
import ssl
from configparser import ConfigParser
from datetime import datetime
from email.mime.text import MIMEText
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))

############################################################
# CONFIGURATION - USE THIS SECTION TO CUSTOMIZE YOUR REPORTS
############################################################

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

# CVEs published/modified before the DATE will not be included in mail
DATE = "01/01/1990" # Mandatory, format dd/mm/yyyy

# Filters to use, please comment unused parameters
CVE_FILTERS = {
            "level": "level_critical", #level_critical = CVSS score > 9, level_high = 7 < 9, level_medium = 4 < 7
            "active": "true",
            # "technology_product": "",
            "groups": ["", ""] # ( ["group"] or ["groupA", "groupB", "groupC"]...)
        }

############################################################

print("! Testing communication with Cyberwatch API")
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))
API_URL = CONF.get('cyberwatch', 'url')

CLIENT.ping()

def sort_servers(full_cve):
    '''Find servers with group filters and not patched CVE'''
    servers_with_groups = []
    print(full_cve.cve_code)
    for server in full_cve.servers:
        if server.active is True:
            server_full = CLIENT.server(str(server.id))
            if "groups" in CVE_FILTERS:
                for group in server_full.groups:
                    if group.name in CVE_FILTERS["groups"]:
                        servers_with_groups.append(server_full)
            else:
                servers_with_groups.append(server_full)

    return servers_with_groups

def sort_cves():
    '''Filter CVEs and generate data for mail'''
    data_for_mail = []

    for cve in CLIENT.cve_announcements(CVE_FILTERS):
        full_cve = CLIENT.cve_announcement(cve.cve_code)

        if full_cve.last_modified is not None:
            last_modified = datetime.strptime(full_cve.last_modified, '%Y-%m-%dT%H:%M:%S.000%z').strftime('%d/%m/%Y')
        elif full_cve.published is not None:
            last_modified = datetime.strptime(full_cve.published, '%Y-%m-%dT%H:%M:%S.000%z').strftime('%d/%m/%Y')
        else:
            continue

        if datetime.strptime(last_modified, '%d/%m/%Y') > datetime.strptime(DATE, '%d/%m/%Y'):
            servers_list = sort_servers(full_cve)
            for server in servers_list:
                data = {
                    "cve_code": cve.cve_code,
                    "published_date": last_modified,
                    "hostname": server.hostname,
                    "os": server.os.name,
                    "score": full_cve.score,
                    "id": server.id
                }
                data_for_mail.append(data)
    return data_for_mail

def build_email(active_cves):
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
<p style="font-size: 16px; line-height: 1.2; word-break: break-word; mso-line-height-alt: 19px; margin: 0;"><span style="font-size: 16px;"><strong>Liste des serveurs vulnérables :<br/></strong></span></p>
</div>
</div>
<div style="font-size:16px;text-align:center;font-family:Arial, Helvetica Neue, Helvetica, sans-serif">
<div style="text-align: center;"> <table class="tg" style="border-collapse:collapse;border-spacing:0;margin-left:auto;margin-right:auto;">
"""
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
    if filtered_active_cves == []:
        html = '<p>Aucun serveur avec une CVE active correspondant aux critères définis a été remonté</p>'
        data = html_start + html + html_end
        return data

    html_start += """
<thead>
<tr>
<th style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">Serveur</th>
<th style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">OS</th>
<th style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">CVE</th>
<th style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">Score</th>
<th style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">Date de publication/modification </th>
</tr>
</thead>
"""
    for line in active_cves:
        html_for_each = """
<tr>
<td style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal"><a href="{}/servers/{}#server_cve_announcements"</a>{}</td>
<td style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">{}</td>
<td style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal"><a href="https://nvd.nist.gov/vuln/detail/{}">{}</a></td>
<td style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;text-align:center;vertical-align:top;word-break:normal">{}</td>
""".format(API_URL, line["id"], line["hostname"], line["os"], line["cve_code"], line["cve_code"], line["score"])

        html_for_each += """
<td style="border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;">{}</td>
""".format(line["published_date"])

        html_start += html_for_each

    html_start += html_end

    return html_start

filtered_active_cves = sort_cves()

HTML = build_email(filtered_active_cves)

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
