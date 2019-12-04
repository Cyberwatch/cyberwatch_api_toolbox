"""Module used to import export file xlsx remote acesses"""

import datetime
import logging
import xlrd
import xlsxwriter

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
                    "node_id": text[titles.index("NODE_ID")],
                    "server_groups" : text[titles.index("SERVER_GROUPS")]
                }

                remote_access = self.client.create_remote_access(info)
                response.append(remote_access)
                logging.debug("Done")

            except ValueError:
                logging.fatal("Error format file xlsx::"
                              "HOST, PORT, TYPE, USERNAME,"
                              "PASSWORD, KEY, NODE_ID, SERVER_GROUPS")
                return None
        return response

    def export_remote_accesses_xlsx(self,
                                    file_xlsx="export_remote_accesses_"+str(
                                        datetime.datetime.now())+".xlsx"):
        """Method to export remote access to an xlsx file"""
        if not file_xlsx or file_xlsx == "":
            logging.error("No xlsx file")
            return False

        if not file_xlsx.endswith(".xlsx"):
            logging.error("Extension not valid")
            return False

        remote_accesses = self.client.remote_accesses()

        logging.debug("Creating file xlsx")
        workbook = xlsxwriter.Workbook(file_xlsx)
        worksheet = workbook.add_worksheet(u"remote_accesses")

        worksheet.write(0, 0, "HOST")
        worksheet.write(0, 1, "PORT")
        worksheet.write(0, 2, "TYPE")
        worksheet.write(0, 3, "NODE_ID")
        worksheet.write(0, 4, "SERVER_GROUPS")

        logging.debug("Add remote accesses in file xlsx")

        i = 1
        for remote_access in remote_accesses:
            worksheet.write(i, 0, remote_access.address)
            worksheet.write(i, 1, remote_access.port)
            worksheet.write(i, 2, remote_access.type)
            worksheet.write(i, 3, remote_access.node_id)

            if remote_access.server_id:
                server = self.client.server(remote_access.server_id)
                if server.groups:
                    group_name = ""
                    for group in server.groups:
                        group_name += group.name + ","
                    group_name = group_name[:-1]
                    worksheet.write(i, 4, group_name)
            i += 1

        workbook.close()
        logging.debug("Done")
        return True
