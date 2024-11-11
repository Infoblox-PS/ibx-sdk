"""
WAPI test module
"""
import logging
import os
import time

import pytest
import urllib3

from ibx_sdk.nios.exceptions import WapiRequestException

log = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
GRID_MGR = os.environ.get('GRID_MGR')
WAPI_VER = os.environ.get('WAPI_VER')
PASSWORD = os.environ.get('PASSWORD')
USERNAME = os.environ.get('USERNAME')
GRID_MEMBER = os.environ.get('GRID_MEMBER')
SSL_VERIFY = False if os.environ.get('SSL_VERIFY') == 'False' else True
CSV_TASK = {}


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
    header-network,address,netmask,comment,network_view,import-action
    network,10.0.0.0,255.255.255.0,vlan-0 patrick-FAKE,,IO
    network,10.0.1.0,255.255.255.0,vlan-1 patrick-FAKE,not_exist,IO
    """
    with open('test.csv', 'w', encoding='utf-8') as file:
        file.write(data)
    file.close()
    res = wapi.csv_import(csv_import_file='test.csv', task_operation='CUSTOM')
    CSV_TASK.update(res)
    os.remove('test.csv')


def test_wapi_csv_task_status(get_wapi):
    wapi = get_wapi
    while True:
        response = wapi.csvtask_status(csvtask=CSV_TASK)
        assert isinstance(response, dict)
        if response.get('status') in ['COMPLETED', 'STOPPED', 'FAILED']:
            break
        time.sleep(5)


def test_wapi_get_csv_errors(get_wapi):
    wapi = get_wapi
    wapi.get_csv_errors_file(
        filename=CSV_TASK['csv_import_task'].get('file_name'),
        job_id=CSV_TASK['csv_import_task'].get('import_id')
    )
    assert os.path.exists(f'csv-errors-{CSV_TASK["csv_import_task"].get("file_name")}.csv')
    os.remove(f'csv-errors-{CSV_TASK["csv_import_task"].get("file_name")}.csv')


def test_wapi_get_log_files(get_wapi):
    wapi = get_wapi
    wapi.get_log_files(log_type='AUDITLOG', node_type='ACTIVE', filename='auditlog.tgz')
    assert os.path.exists('auditlog.tgz')
    os.remove('auditlog.tgz')


def test_wapi_get_support_bundle(get_wapi):
    wapi = get_wapi
    wapi.get_support_bundle(member=GRID_MEMBER, filename='test-support-bundle.tgz')
    assert os.path.exists('test-support-bundle.tgz')
    os.remove('test-support-bundle.tgz')


def test_wapi_member_config(get_wapi):
    wapi = get_wapi
    wapi.member_config(member=GRID_MEMBER, conf_type='DNS_CFG')
    assert os.path.exists('dnsconf.tar.gz')
    os.remove('dnsconf.tar.gz')


def test_wapi_grid_backup(get_wapi):
    wapi = get_wapi
    wapi.grid_backup()
    assert os.path.exists('database.bak')


def test_wapi_grid_restore(get_wapi):
    wapi = get_wapi
    wapi.grid_restore()
    os.remove('database.bak')


def test_wapi_download_certificate(get_wapi):
    wapi = get_wapi
    wapi.download_certificate(
        member=GRID_MEMBER,
        certificate_usage='ADMIN'
    )
    assert os.path.exists('apache_server.crt')
    os.remove('apache_server.crt')


def test_wapi_generate_selfsigned_cert(get_wapi):
    wapi = get_wapi
    wapi.generate_selfsigned_cert(
        member=GRID_MEMBER,
        certificate_usage='ADMIN',
        cn=GRID_MEMBER,
    )
    assert os.path.exists('cert.pem')
    os.remove('cert.pem')


def test_wapi_generate_csr(get_wapi):
    wapi = get_wapi
    wapi.generate_csr(
        member=GRID_MEMBER,
        certificate_usage='ADMIN',
        cn=GRID_MEMBER,
    )
    assert os.path.exists('cert.pem')
    os.remove('cert.pem')


