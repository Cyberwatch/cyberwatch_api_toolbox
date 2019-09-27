"""import file xlsx"""

from cbw_api_toolbox.cbw_file_xlsx import CBWXlsx

API_KEY = ''
SECRET_KEY = ''
API_URL = ''

FILE_XLSX = 'examples/import_file.xlsx'

XLSX = CBWXlsx(API_URL, API_KEY, SECRET_KEY)

RESPONSE = XLSX.import_remote_accesses_xlsx(FILE_XLSX)

if RESPONSE:
    for remote_access in RESPONSE:
        if remote_access:
            print("remote access created, id=>>>>>{}".format(remote_access.id))
        else:
            print("An error occurred, import_remote_accesses_xlsx failed")
else:
    print("Error format file xlsx::HOST, PORT, TYPE, USERNAME, PASSWORD, KEY, NODE, GROUPS,  COMPLIANCE_GROUPS")
