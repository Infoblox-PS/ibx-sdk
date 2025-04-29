import logging
import pytest

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    logging.getLogger().setLevel(logging.DEBUG)
