"""Script that sends an email report with the 10 most important CVEs and some of there attributes"""
import smtplib
import ssl
from collections import defaultdict
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cbw_api_toolbox.cbw_api import CBWApi

# SMTP Configuration
SENDER_EMAIL = "noreply@cyberwatch.fr"
RECEIVER_EMAILS = ["", ""]
LOGIN_SMTP = ""
PASSWORD_SMTP = ""
SMTP_SERVER = ""
PORT_SMTP = 465

# API Configuration
API_KEY = ""
SECRET_KEY = ""
API_URL = ""
CLIENT = CBWApi(API_URL, API_KEY, SECRET_KEY)

# Filters
MIN_SCORE = 8


def sort_by_keys(count, score, exploit_available):
    """
        Return formatted string with digits to be used by sorted() to sort by keys
    """
    format_sort = "{}_".format(
        exploit_available[0]) + "{0:0=4d}".format(int(score)) + "_{0:0=4d}".format(count)
    return format_sort


CVE_COUNTS = defaultdict(int)
CVE_LIST = {}

for server_item in CLIENT.servers():
    server = CLIENT.server(server_item.id)
    if server.cve_announcements is not None:
        for cve_announcement in server.cve_announcements:
            if cve_announcement.cve_score is not None:
                CVE_COUNTS[cve_announcement.cve_code] += 1
                if cve_announcement.cve_score >= MIN_SCORE:
                    CVE_LIST[cve_announcement.cve_code] = {
                        "count": CVE_COUNTS[cve_announcement.cve_code],
                        "cve_score": cve_announcement.cve_score,
                        "published": cve_announcement.published
                    }

#Check if cve has a public exploit
for cve_code in CVE_LIST:
    cve = CLIENT.cve_announcement(cve_code)
    CVE_LIST[cve_code]["exploitable"] = str(cve.exploitable)

SORTED_CVES = sorted(CVE_LIST.items(), reverse=True,
                     key=lambda kv: sort_by_keys(kv[1]["count"], kv[1]["cve_score"], kv[1]["exploitable"]))

# Email Configuration
MESSAGE = MIMEMultipart("alternative")
MESSAGE["Subject"] = "Rapport Cyberwatch - " +  date.today().strftime("%m/%d/%y")
MESSAGE["From"] = SENDER_EMAIL
MESSAGE["To"] = ", ".join(RECEIVER_EMAILS)

# Create HTML version of your message
CONTENT = f''''''
for i in range(10):
    CVE_SCORE = SORTED_CVES[i][1]['cve_score']
    CVE_CODE = SORTED_CVES[i][0]
    PUBLISHED_DATE = SORTED_CVES[i][1]['published'][:10]
    HAS_EXPLOIT = "disponible" if SORTED_CVES[i][1]['exploitable'] else "non-disponible"
    IMPACTED_MACHINES_FORMAT = " machines impactées)" if SORTED_CVES[i][1]['count'] > 1 else " machine impactée)"
    IMPACTED_MACHINES_COUNT = str(SORTED_CVES[i][1]["count"]) + IMPACTED_MACHINES_FORMAT
    CONTENT += f"""{i+1}. {CVE_CODE} (score CVSS {CVE_SCORE},
    publiée le {PUBLISHED_DATE},
    exploit public {HAS_EXPLOIT},
    {IMPACTED_MACHINES_COUNT}
     - <a href="{API_URL}/vulnerabilities/{CVE_CODE}">Voir détails</a><br/>"""

EMAIL_BODY = f"""\
<p>Bonjour,</p>

<p>merci de bien vouloir trouver ci-après le top 10 des CVEs détectées sur votre parc.</p>

<p>{CONTENT}</p>

<p>Très cordialement,</p>

<p>L'équipe Cyberwatch - support@cyberwatch.fr</p>
"""

# Turn these into plain/html MIMEText objects
PART1 = MIMEText(EMAIL_BODY, "plain")
PART2 = MIMEText(EMAIL_BODY, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
MESSAGE.attach(PART1)
MESSAGE.attach(PART2)

# Create secure connection with server and send email
CONTEXT = ssl.create_default_context()
with smtplib.SMTP_SSL(SMTP_SERVER, PORT_SMTP, context=CONTEXT) as server:
    server.login(LOGIN_SMTP, PASSWORD_SMTP)
    server.sendmail(
        SENDER_EMAIL, RECEIVER_EMAILS, MESSAGE.as_string()
    )
