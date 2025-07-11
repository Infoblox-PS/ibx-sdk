<img alt="Professional Services" src="https://raw.githubusercontent.com/Infoblox-PS/ibx-sdk/main/src_docs/assets/ibx-sdk-img.png" title="Infoblox Professional Services"/>

# Table of Contents

1. [NIOS API](#nios-api)
2. [Overview](#overview)

# Overview

Welcome to the `ibx-sdk` for Infoblox Products. This SDK contains the following:

* Python wrapper for Infoblox NIOS Web RESTful API or WAPI
* Suite of core Python scripts and tools
* Full documentation

The `ibx-sdk` is a designed collection of Python classes and methods tailored for streamlined and effective interaction.
This SDK is developed with a focus on simplicity and efficiency, enabling users to perform a variety of API actions 
essential for integrations with Infoblox Products.

The `ibx-sdk` is crafted to accommodate users at different levels of expertise. It offers an intuitive interface for 
beginners, while still providing the robust functionality that experienced developers require. The SDK is an ideal 
solution for automating network management tasks, ensuring seamless integration with diverse systems and workflows.

Included in this SDK are several practical script and tools that illustrate the application of its methods in real-world 
scenarios. These scripts are intended to provide users with a clear understanding of how the toolkit can be utilized to 
its full potential, demonstrating its versatility and effectiveness in various use cases.

We invite you to explore the capabilities of the `ibx-sdk`. Our goal is to deliver an SDK that is not only reliable and 
efficient but also adaptable to the dynamic requirements of contemporary network environments.

# Contributing

## Testing

Testing is a requirement for contributing code to this project. You're expected to write test cases which "covers" your 
code additions, changes, and/or deletions. This section describes how to set up, configure, and implement testing of the 
`ibx-sdk`.

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

It's recommended that you configure your own env variables. The best, safest, and easiest way is to
create a `.env` file at the root of the project. Create the file with the following variables:

```dotenv
GRID_MGR=192.168.1.2
USERNAME=admin
PASSWORD=infoblox
SSL_VERIFY=False
WAPI_VER=2.12
```

The above is a sample file only - please update it with sane values according to your testing
environment.

### Running Tests

To run tests, perform the following from the root of the project:

```shell
coverage run -m pytest -svvv
```

You should see output like the following:

```shell
(.venv) ➜  ibx-sdk git:(dev-ppiper) ✗ coverage run -m pytest -svvv
============================================== test session starts ===============================================
platform darwin -- Python 3.10.13, pytest-7.4.3, pluggy-1.3.0 -- /Users/ppiper/workspace/ibx-sdk/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/ppiper/workspace/ibx-sdk
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

Once you run the test suite, you can examine the code coverage of the tests - always strive for
100%:

```shell
coverage report
```

or

```shell
coverage report -m
```

```shell
(.venv) ➜  ibx-sdk git:(dev-ppiper) ✗ coverage report
Name                                          Stmts   Miss  Cover
-----------------------------------------------------------------
src/ibx_sdk/__init__.py                         0      0   100%
src/ibx_sdk/nios/__init__.py                    0      0   100%
src/ibx_sdk/nios/fileop.py                    359    335     7%
src/ibx_sdk/nios/service.py                    42     35    17%
src/ibx_sdk/nios/wapi.py                      125     59    53%
src/ibx_sdk/util/__init__.py                    0      0   100%
src/ibx_sdk/util/util.py                      167    149    11%
tests/wapi/__init__.py                            0      0   100%
tests/wapi/test_env_variables_pytest_env.py       8      0   100%
tests/wapi/test_wapi.py                          50      0   100%
-----------------------------------------------------------------
TOTAL                                           751    578    23%
```

This shows we're only hitting 53% of the WAPI code in our testing. 
