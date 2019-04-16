"""Module used to import export file xlsx remote acesses"""

import logging
import xlrd
from cbw_api_toolbox.cbw_api import CBWApi

class CBWXlsx:
    """Class used to import/export file xlsx remote acesses"""

    def __init__(self, api_url, api_key, secret_key):
        self.client = CBWApi(api_url, api_key, secret_key)

    def import_remote_accesses_xlsx(self, file_xlsx):
        """method to import remote accesses from an xlsx file"""
        if not file_xlsx:
            logging.fatal("No Files xlsx")
            return None

        if not file_xlsx.endswith(".xlsx"):
            logging.fatal("Extension not valid")
            return None

        imported = xlrd.open_workbook(file_xlsx)
        lines = imported.sheet_by_index(0)
        response = []
        titles = lines.row_values(0)

        for line in range(1, lines.nrows):
            text = lines.row_values(line)
            address = lines.row_values(line)[0]
            logging.debug("Creating remote access {}".format(address))

            try:
                info = {
                    "address": text[titles.index("HOST")],
                    "port": text[titles.index("PORT")],
                    "type": text[titles.index("TYPE")],
                    "login": text[titles.index("USERNAME")],
                    "password": text[titles.index("PASSWORD")],
                    "key": text[titles.index("KEY")],
                    "node": text[titles.index("NODE")]
                }
            except ValueError:
                logging.fatal("Error format file xlsx::"
                              "HOST, PORT, TYPE, USERNAME, PASSWORD, KEY, NODE, GROUPS")
                return None

            remote_access = self.client.create_remote_access(info)
            response.append(remote_access)
            logging.debug("Add groups for server")

            if (titles.index("GROUPS") and remote_access
                    and remote_access.address == info["address"]):
                self.client.update_server(remote_access.server.id, text[titles.index("GROUPS")])
                logging.debug("Groups successfully added")
            logging.debug("Done")
        return response
