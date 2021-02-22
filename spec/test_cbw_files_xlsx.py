"""Test file for cbw_files_xlsx.py"""

import openpyxl  # pylint: disable=import-error
import vcr  # pylint: disable=import-error
from cbw_api_toolbox.cbw_file_xlsx import CBWXlsx

# To generate a new vcr cassette:
# - DO NOT CHANGE THE API_URL
# - Add your local credentials API_KEY and SECRET_KEY
# - Execute the test a first time, it should generate the cassette
# - Remove your credentials
# - relaunch the test. everything should work.


API_KEY = ''
SECRET_KEY = ''
API_URL = 'https://localhost'


class TestCBWXlsx:
    """Test for class CBWFilsXlsx"""

    @staticmethod
    def test_import_remote_accesses_xlsx():
        """Tests for method import_xls"""
        client = CBWXlsx(API_URL, API_KEY, SECRET_KEY)
        file_xlsx = "spec/fixtures/xlsx_files/batch_import_model.xlsx"

        remote_accesses_validate = [
            "cbw_object(id=17, type='CbwRam::RemoteAccess::Ssh::WithPassword', \
address='10.0.2.15', port=22, is_valid=None, last_error=None, server_id=None, node_id=1)",
            "cbw_object(id=18, type='CbwRam::RemoteAccess::Ssh::WithPassword', address='server02.example.com', \
port=22, is_valid=None, last_error=None, server_id=None, node_id=1)",
            "cbw_object(id=19, type='CbwRam::RemoteAccess::Ssh::WithPassword', address='server01.example.com', port=22\
, is_valid=None, last_error=None, server_id=None, node_id=1)"]

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/'
                              'import_remote_accesses_xlsx_file.yaml'):
            response = client.import_remote_accesses_xlsx(file_xlsx)

            assert len(response) == 3

            assert str(response[0]) == remote_accesses_validate[0]
            assert str(response[1]) == remote_accesses_validate[1]
            assert str(response[2]) == remote_accesses_validate[2]

        file_xlsx = "spec/fixtures/xlsx_files/batch_import_model_false.xlsx"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/'
                              'import_remote_accesses_xlsx_file_false.yaml'):
            response = client.import_remote_accesses_xlsx(file_xlsx)

            assert len(response) == 3
            assert response[0] is False
            assert response[1] is False
            assert str(response[2]), remote_accesses_validate[2]

    @staticmethod
    def test_export_remote_accesses_xlsx():
        """Tests for export remote accesses xlsx file method"""
        client = CBWXlsx(API_URL, API_KEY, SECRET_KEY)

        file_xlsx = "test.xlsx"
        with vcr.use_cassette('spec/fixtures/vcr_cassettes/export_file_xlsx.yaml'):
            response = client.export_remote_accesses_xlsx(file_xlsx)

            workbook = openpyxl.load_workbook(file_xlsx)
            worksheet = workbook.active
            result = []

            for cell in worksheet[1]:
                result.append(cell.value)
            assert response is True and result == [
                'HOST', 'PORT', 'TYPE', 'NODE_ID', 'SERVER_GROUPS']

            result = []
            for cell in worksheet[5]:
                result.append(cell.value)

            # The group is not assigned yet
            assert result == ['10.0.2.15', 22,
                              'CbwRam::RemoteAccess::Ssh::WithPassword', 1, None]
