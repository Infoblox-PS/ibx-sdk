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
GRID_MEMBER = os.environ.get('GRID_MEMBER')
SSL_VERIFY = False if os.environ.get('SSL_VERIFY') == 'False' else True
CSV_TASK = {}


def test_wapi_service_status(get_wapi):
    wapi = get_wapi
    response = wapi.get_service_restart_status()
    assert isinstance(response, list)


def test_wapi_update_service_status(get_wapi):
    wapi = get_wapi
    wapi.update_service_status()


def test_wapi_service_restart(get_wapi):
    wapi = get_wapi
    wapi.service_restart()
