<img alt="Professional Services" src="docs/assets/ib-toolkit-img.png" title="Infoblox Professional Services"/>

# Table of Contents

1. [NIOS API](#nios-api)
2. [Overview](#overview)

# Overview

A collection of basic tools and functions used by other integrations written by Infoblox Professional Services. This
collection also contains scripts that perform various functions. These scripts are written as functioning examples.

# NIOS API

## WAPI Module Overview

The `wapy.py` is a Python class library designed for interacting with the Infoblox NIOS Web API (WAPI). The primary
class,
`WAPI`, extends `requests.sessions.Session` and provides functionalities for session management, data retrieval, file
operations, and service management

## FILEOP Module Overview

The `fileop.py` module provides a suite of functions for managing file operations in the context of the Infoblox Web
API (WAPI). These functions are designed to be used within the `WAPI` class and handle various file-related tasks
such as configuration file downloads, CSV exports and imports, grid backups and restorations, and log file management.


## Grid Services Module Overview

The `Grid Services` module in Python provides functions to interact with and manage services in an Infoblox Grid
environment. It includes capabilities to restart services, update their status, and retrieve the status of service
restarts.

# Contributing

## Testing

Testing is a requirement for contributing code to this project. You're expected to write test cases which "covers" your
code additions, changes, and/or deletions. This section describes how to setup, configure and implement testing of the 
Basic API Toolkit.

### Software Requirements

Install the following set of Python modules for testing:
* coverage
* pytest
* pytest-env
* pytest-dotenv

This is done as follows:

```shell
pip install pytest pytest-env pytest-dotenv coverage
```

### Testing Configuration

It's recommended that you configure your own env variables. The best, safest, and easiest way is to create a `.env` file
at the root of the project. Create the file with the following variables:

```dotenv
GRID_MGR=192.168.1.2
USERNAME=admin
PASSWORD=infoblox
SSL_VERIFY=False
WAPI_VER=2.12
```

The above is a sample file only - please update it with sane values according to your testing environment. 

### Running Tests

To run tests, perform the following from the root of the project:

```shell
coverage run -m pytest -svvv
```

You should see output like the following:
```shell
(.venv) ➜  ibx-tools git:(dev-ppiper) ✗ coverage run -m pytest -svvv
============================================== test session starts ===============================================
platform darwin -- Python 3.10.13, pytest-7.4.3, pluggy-1.3.0 -- /Users/ppiper/workspace/ibx-tools/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/ppiper/workspace/ibx-tools
configfile: pytest.ini
plugins: env-1.1.3, dotenv-0.5.2
collected 9 items

tests/wapi/test_env_variables_pytest_env.py::test_env_variables_pytest_env PASSED
tests/wapi/test_wapi.py::test_instantiate_wapi_without_properties PASSED
tests/wapi/test_wapi.py::test_instantiate_wapi_with_positional_arguments PASSED
tests/wapi/test_wapi.py::test_instantiate_wapi_with_named_arguments PASSED
tests/wapi/test_wapi.py::test_instantiate_wapi_with_dictionary_of_arguments PASSED
tests/wapi/test_wapi.py::test_ssl_verify_as_string_value PASSED
tests/wapi/test_wapi.py::test_ssl_verify_as_boolean_value PASSED
tests/wapi/test_wapi.py::test_wapi_basic_auth_connection PASSED
tests/wapi/test_wapi.py::test_wapi_basic_auth_connection_with_bad_password PASSED

=============================================== 9 passed in 0.10s ================================================
```

Once you run the test suite, you can examine the code coverage of the tests - always strive for 100%:
```shell
coverage report
```

or 

```shell
coverage report -m
```

```shell
(.venv) ➜  ibx-tools git:(dev-ppiper) ✗ coverage report
Name                                          Stmts   Miss  Cover
-----------------------------------------------------------------
src/ibx_tools/__init__.py                         0      0   100%
src/ibx_tools/nios/__init__.py                    0      0   100%
src/ibx_tools/nios/fileop.py                    359    335     7%
src/ibx_tools/nios/service.py                    42     35    17%
src/ibx_tools/nios/wapi.py                      125     59    53%
src/ibx_tools/util/__init__.py                    0      0   100%
src/ibx_tools/util/util.py                      167    149    11%
tests/wapi/__init__.py                            0      0   100%
tests/wapi/test_env_variables_pytest_env.py       8      0   100%
tests/wapi/test_wapi.py                          50      0   100%
-----------------------------------------------------------------
TOTAL                                           751    578    23%
```

This shows we're only hitting 53% of the WAPI code in our testing. 
