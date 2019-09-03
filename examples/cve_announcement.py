"""GET request to /api/v2/cve_announcements/{CVE_CODE} to get all informations
about a specific cve_announcement"""
from cbw_api_toolbox.cbw_api import CBWApi

API_KEY = ''
SECRET_KEY = ''
API_URL = ''

CLIENT = CBWApi(API_URL, API_KEY, SECRET_KEY)

CVE_CODE = 'CVE-2017-0146'

CLIENT.cve_announcement(CVE_CODE)
