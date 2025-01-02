"""
WAPI test module
"""
from random import randint

from ibx_sdk.logger.ibx_logger import init_logger, CallCounted

LOG = init_logger(
    level='DEBUG',
    logfile_mode='w',
    logfile_name='test.log',
    console_log=True,
)
LOG.debug = CallCounted(LOG.debug)
LOG.info = CallCounted(LOG.info)
LOG.warning = CallCounted(LOG.warning)
LOG.error = CallCounted(LOG.error)
LOG.critical = CallCounted(LOG.critical)


def test_random_log_counts():
    calls = [
        {"call": LOG.debug, "count": randint(1, 10), "msg": "This is a debug log"},
        {"call": LOG.info, "count": randint(1, 10), "msg": "This is an info log"},
        {"call": LOG.warning, "count": randint(1, 10), "msg": "This is a warning log"},
        {"call": LOG.error, "count": randint(1, 10), "msg": "This is an error log"},
        {"call": LOG.critical, "count": randint(1, 10), "msg": "This is a critical log"},
    ]
    for call in calls:
        for _ in range(call["count"]):
            call["call"](call["msg"])

    assert LOG.debug.counter == calls[0]["count"]
    assert LOG.info.counter == calls[1]["count"]
    assert LOG.warning.counter == calls[2]["count"]
    assert LOG.error.counter == calls[3]["count"]
    assert LOG.critical.counter == calls[4]["count"]

def test_console_debug_log():
    LOG.debug("DEBUG = %s", LOG.debug.counter)

def test_console_info_log():
    LOG.info("INFO = %s", LOG.info.counter)

def test_console_warning_log():
    LOG.warning("WARNING = %s", LOG.warning.counter)

def test_console_error_log():
    LOG.error("ERROR = %s", LOG.error.counter)

def test_console_critical_log():
    LOG.critical("CRITICAL = %s", LOG.critical.counter)
