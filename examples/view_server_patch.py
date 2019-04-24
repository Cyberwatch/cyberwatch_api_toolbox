"""view the server patch"""

from cbw_api_toolbox.cbw_api import CBWApi

API_KEY = ""
SECRET_KEY = ""
API_URL = ""

CLIENT = CBWApi(API_URL, API_KEY, SECRET_KEY)

SERVER_ID = "" # add the server id

server = CLIENT.server(SERVER_ID)

print("Server : {}".format(server.hostname))
print("Update count : {}".format(server.updates_count))

print("Updates :")
for update in server.updates:
    print("\t-Product : {0}\n"
          "\t\t- Corrective action : {1} -> {2}".format(update["current"]["product"],
                                                        update["current"]["version"],
                                                        update["target"]["version"]))

    cve_list = ""
    for cve in update["cve_announcements"]:
        cve_list = cve_list + cve["cve_code"] + ", "

    print("\t\t- Cve List : {}".format(cve_list[:-2]))
