from cbw_api_toolbox.cbw_api import CBWApi

API_KEY = ''
SECRET_KEY = ''
API_URL = ''

servers = CBWApi(API_URL, API_KEY, SECRET_KEY).get_detailed_servers()

category_by_groups = {}

# append each server to a group by category dict
for server in servers:
    if server.groups:
        for group in server.groups:
            if group.name not in category_by_groups:
                category_by_groups[group.name] = {}

            concerned_group = category_by_groups[group.name]

            if server.category not in concerned_group:
                concerned_group[server.category] = []

            concerned_group[server.category].append(server)

for group in category_by_groups:
    print(f"--- GROUP : {group} ---")

    for category in category_by_groups[group]:
        print(f"{category}  : {len(category_by_groups[group][category])}")
