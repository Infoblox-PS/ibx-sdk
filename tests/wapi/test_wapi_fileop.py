"""
WAPI test module
"""
import logging
import os

import pytest
import urllib3

from ibx_tools.nios.exceptions import WapiRequestException

log = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
GRID_MGR = os.environ.get('GRID_MGR')
WAPI_VER = os.environ.get('WAPI_VER')
PASSWORD = os.environ.get('PASSWORD')
USERNAME = os.environ.get('USERNAME')
SSL_VERIFY = False if os.environ.get('SSL_VERIFY') == 'False' else True


def test_wapi_csv_import_file_not_exist(get_wapi):
    wapi = get_wapi
    with pytest.raises(FileNotFoundError) as err:
        wapi.csv_import(task_operation='CUSTOM', csv_import_file='file_not_exist.csv')
        assert err == "FileNotFoundError: [Errno 2] No such file or directory: 'file_not_exist.csv'"


def test_wapi_csv_export(get_wapi):
    wapi = get_wapi
    wapi.csv_export(wapi_object='zone_auth', filename='test.csv')
    assert os.path.isfile('test.csv')
    os.remove('test.csv')


def test_wapi_csv_export_unsupported_object(get_wapi):
    wapi = get_wapi
    with pytest.raises(WapiRequestException):
        wapi.csv_export(wapi_object='networkcontainer', filename='test.csv')


def test_wapi_csv_export_with_no_filename(get_wapi):
    wapi = get_wapi
    wapi.csv_export(wapi_object='zone_auth')
    assert os.path.isfile('authzones.csv')
    os.remove('authzones.csv')


def test_wapi_csv_import_networks_custom_load(get_wapi):
    wapi = get_wapi
    data = """
    header-network,address,netmask,comment,import-action
    network,10.0.0.0,255.255.255.0,vlan-0 patrick-FAKE,IO
    network,10.0.1.0,255.255.255.0,vlan-1 patrick-FAKE,IO
    """
    with open('test.csv', 'w', encoding='utf-8') as file:
        file.write(data)
        wapi.csv_import(csv_import_file='test.csv', task_operation='CUSTOM')
    file.close()
    os.remove('test.csv')
