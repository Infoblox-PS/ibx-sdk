"""
WAPI test module
"""
import logging
import os

import urllib3

log = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
GRID_MGR = os.environ.get('GRID_MGR')
WAPI_VER = os.environ.get('WAPI_VER')
PASSWORD = os.environ.get('PASSWORD')
USERNAME = os.environ.get('USERNAME')
SSL_VERIFY = False if os.environ.get('SSL_VERIFY') == 'False' else True


def test_wapi_csv_export(get_wapi):
    wapi = get_wapi
    wapi.csv_export(wapi_object='network', filename='test.csv')
    assert os.path.isfile('test.csv')
