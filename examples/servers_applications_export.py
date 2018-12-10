import xlsxwriter

from cbw_api_toolbox.cbw_api import CBWApi

"""
FOR THIS EXAMPLE YOU NEED TO INSTALL xlsxwriter : 
    pip3 install xlsxwriter
"""

API_KEY = ''
SECRET_KEY = ''
API_URL = ''

servers = CBWApi(API_URL, API_KEY, SECRET_KEY).get_detailed_servers()

exported = xlsxwriter.Workbook('cbw_export_servers_applications.xlsx')

for server in servers:
    if server.applications:
        print(f"Export applications for {server.hostname}")

        worksheet = exported.add_worksheet(server.hostname)

        worksheet.write(0, 0, "Application")
        worksheet.write(0, 1, "Version")

        row = 1
        col = 0

        for application in server.applications:
            worksheet.write(row, col, application.product)
            worksheet.write(row, col + 1, application.version)
            row += 1

exported.close()
