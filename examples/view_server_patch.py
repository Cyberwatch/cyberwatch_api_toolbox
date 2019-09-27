"""View the server updates"""

from cbw_api_toolbox.cbw_api import CBWApi

API_KEY = ""
SECRET_KEY = ""
API_URL = ""

CLIENT = CBWApi(API_URL, API_KEY, SECRET_KEY)

SERVER_ID = ""  # add the server id

SERVER = CLIENT.server(SERVER_ID)

print("Server : {}".format(SERVER.hostname))
print("Update count : {}".format(SERVER.updates_count))

print("Updates :")
for update in SERVER.updates:
    print("\t-Product : {}".format(update["current"]["product"]))
    print("\t\t- Corrective action : {0} -> {1}".format(update["current"]["version"],
                                                        update["target"]["version"]))

    cve_list = []
    for cve in update["cve_announcements"]:
        cve_list.append(cve["cve_code"])

    print("\t\t- Cve List : {}".format(", ".join(cve_list)))
