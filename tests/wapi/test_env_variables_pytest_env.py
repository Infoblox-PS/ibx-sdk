"""
test cases for pytest-env variables
"""
import os


def test_env_variables_pytest_env():
    grid_mgr = os.environ.get('GRID_MGR')
    username = os.environ.get('USERNAME')
    ssl_verify = False if os.environ.get('SSL_VERIFY') == 'False' else True
    assert grid_mgr == '192.168.40.60'
    assert username == 'admin'
    assert ssl_verify is False
