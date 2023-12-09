"""
conftest.py - shared fixtures
"""
import os

import pytest

from ibx_tools.nios.wapi import WAPI

GRID_MGR = os.environ.get('GRID_MGR')
WAPI_VER = os.environ.get('WAPI_VER')
PASSWORD = os.environ.get('PASSWORD')
USERNAME = os.environ.get('USERNAME')
SSL_VERIFY = False if os.environ.get('SSL_VERIFY') == 'False' else True


@pytest.fixture(scope='session')
def get_wapi():
    """
    This method sets up and returns an instance of the WAPI class for API communication.

    Usage:
        wapi = get_wapi()

    Returns:
        WAPI: An instance of the WAPI class.

    """
    wapi = WAPI(grid_mgr=GRID_MGR, wapi_ver=WAPI_VER, ssl_verify=SSL_VERIFY)
    wapi.connect(username=USERNAME, password=PASSWORD)
    yield wapi

