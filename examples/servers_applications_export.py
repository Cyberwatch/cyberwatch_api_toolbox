"""Example: Export the applications for each servers"""

# FOR THIS EXAMPLE YOU NEED TO INSTALL xlsxwriter : pip3 install xlsxwriter
import xlsxwriter  # pylint: disable=import-error

from cbw_api_toolbox.cbw_api import CBWApi

API_KEY = ''
SECRET_KEY = ''
API_URL = ''

CLIENT = CBWApi(API_URL, API_KEY, SECRET_KEY)

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

        row = 1
        col = 0

        for application in server.applications:
            worksheet.write(row, col, application.product)
            worksheet.write(row, col + 1, application.version)
            row += 1

EXPORTED.close()
