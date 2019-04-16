"""Test file for cbw_files_xlsx.py"""

from cbw_api_toolbox.cbw_objects.cbw_remote_access import CBWRemoteAccess
from cbw_api_toolbox.cbw_file_xlsx import CBWXlsx

import vcr  # pylint: disable=import-error

# To generate a new vcr cassette:
# - DO NOT CHANGE THE API_URL
# - Add your local credentials API_KEY and SECRET_KEY
# - Execute the test a first time, it should generate the cassette
# - Remove your credentials
# - relaunch the test. everything should work.


API_KEY = ''
SECRET_KEY = ''
API_URL = 'http://localhost'


class TestCBWXlsx:
    """Test for class CBWFilsXlsx"""

    @staticmethod
    def test_import_remote_accesses_xlsx():
        """Tests for method import_xls"""
        client = CBWXlsx(API_URL, API_KEY, SECRET_KEY)
        file_xlsx = "spec/fixtures/xlsx_files/batch_import_model.xlsx"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/'
                              'import_remote_accesses_xlsx_file.yaml'):
            response = client.import_remote_accesses_xlsx(file_xlsx)

            assert len(response) == 3
            assert isinstance(response[0], CBWRemoteAccess) is True
            assert isinstance(response[1], CBWRemoteAccess) is True
            assert isinstance(response[2], CBWRemoteAccess) is True

        file_xlsx = "spec/fixtures/xlsx_files/batch_import_model_false.xlsx"

        with vcr.use_cassette('spec/fixtures/vcr_cassettes/'
                              'import_remote_accesses_xlsx_file_false.yaml'):
            response = client.import_remote_accesses_xlsx(file_xlsx)

            assert len(response) == 3
            assert isinstance(response[0], CBWRemoteAccess) is False
            assert isinstance(response[1], CBWRemoteAccess) is False
            assert isinstance(response[2], CBWRemoteAccess) is True
