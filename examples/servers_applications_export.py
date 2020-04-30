"""Example: Export the applications for each servers"""

import os
from configparser import ConfigParser
import xlsxwriter  # pylint: disable=import-error
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

CLIENT.ping()

SERVERS = CLIENT.servers()

EXPORTED = xlsxwriter.Workbook('cbw_export_servers_applications.xlsx')

for server in SERVERS:
    server = CLIENT.server(server.id)

    if server and server.applications:
        print("Export applications for {0}".format(server.hostname))

        worksheet = EXPORTED.add_worksheet(server.hostname)

        worksheet.write(0, 0, "Application")
        worksheet.write(0, 1, "Version")

        ROW = 1
        COL = 0

        for application in server.applications:
            worksheet.write(ROW, COL, application.product)
            worksheet.write(ROW, COL + 1, application.version)
            Row += 1

EXPORTED.close()
