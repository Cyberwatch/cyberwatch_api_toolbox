"""Export remote accesses in file xlsx"""

from cbw_api_toolbox.cbw_file_xlsx import CBWXlsx

API_KEY = ''
SECRET_KEY = ''
API_URL = ''

FILE_XLSX = "" #Optional parameter

XLSX = CBWXlsx(API_URL, API_KEY, SECRET_KEY)

print(XLSX.export_remote_accesses_xlsx())
