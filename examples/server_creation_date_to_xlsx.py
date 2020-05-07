"""
Get machines and the date they were created.

Require Python 3.7.5 or higher
"""

import os
from configparser import ConfigParser
from datetime import datetime
import xlsxwriter  # pylint: disable=import-error
from cbw_api_toolbox.cbw_api import CBWApi

CONF = ConfigParser()
CONF.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'api.conf'))
CLIENT = CBWApi(CONF.get('cyberwatch', 'url'), CONF.get('cyberwatch', 'api_key'), CONF.get('cyberwatch', 'secret_key'))

def server_list_created():
    """Generate the xls workbook."""
    workbook = xlsxwriter.Workbook('export.xlsx', {'remove_timezone': True})
    row = 0
    col = 0

    # Initiating xls file
    computer_workbook = workbook.add_worksheet("Computers")
    computer_workbook.write(row, col, "Hostname")
    computer_workbook.write(row, col + 1, "Creation Date")

    date_format = workbook.add_format({'num_format': 'dd/mm/yy hh:mm', 'align': 'left'})

    # Write for each Host and it's creation date in `Computers` tab
    for server in CLIENT.servers():

        creation_date = datetime.strptime(server.created_at, '%Y-%m-%dT%H:%M:%S.%f%z')

        computer_workbook.write(row + 1, col, server.hostname)
        computer_workbook.write_datetime(row + 1, col + 1, creation_date, date_format)

        row += 1

    workbook.close()

#Test the client connexion
print("Testing connexion")
CLIENT.ping()

#Lauching server_list_created
server_list_created()
print("XLS file created")
