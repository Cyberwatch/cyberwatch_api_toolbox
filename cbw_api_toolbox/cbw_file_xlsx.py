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

    @classmethod
    def __address_already_taken(cls, address, remote_accesses):
        """method to check if a remote access already exists with the same IP address"""
        for remote_access in remote_accesses:
            if remote_access.address == address:
                logging.info("Address {} already taken, affecting groups to existing server".format(address))
                return remote_access
        return False

    def __find_group_by_name(self, group_name):
        """method to find a group id by its name, create and return the new group"""
        groups = self.client.groups()
        for group in groups:
            if group.name == group_name:
                return group.id
        # If the group is not found, create it
        parameters = {"name": group_name}
        group = self.client.create_group(parameters)
        return group.id

    def __affect_group_remote_access_server(self, remote_access, groups):
        """method to affect groups to a remote_access' server"""
        if not remote_access or not remote_access.server_id:
            return

        server = self.client.server(str(remote_access.server_id))

        group_ids = []
        for group in server.groups:
            group_ids.append(group.id)

        for group_name in groups.split(','):
            if group_name.strip() != '':
                group_ids.append(self.__find_group_by_name(group_name.strip()))

        parameters = {"groups": group_ids}
        self.client.update_server(str(server.id), parameters)

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
        remote_accesses = self.client.remote_accesses()

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

                # Get the list of remote accesses once to reuse
                remote_access = self.client.create_remote_access(info)

                # Check if the remote access already exists and add groups to the corresponding server
                if remote_access is False:
                    remote_access = self.__address_already_taken(address, remote_accesses)
                    self.__affect_group_remote_access_server(remote_access, text[titles.index("SERVER_GROUPS")])

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
