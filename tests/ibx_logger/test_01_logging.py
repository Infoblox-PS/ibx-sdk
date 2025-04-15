"""
WAPI test module
"""

from random import randint

from ibx_sdk.logger.ibx_logger import init_logger, CountingHandler

LOG = init_logger(
    logfile_mode="w",
    logfile_name="test.log",
    level="DEBUG",
    console_log=True,
)
COUNTING_HANDLER = CountingHandler()
LOG.addHandler(COUNTING_HANDLER)


def test_random_log_counts():
    calls = [
        {"call": LOG.debug, "count": randint(1, 10), "msg": "This is a debug log",
         "level": "DEBUG"},
        {"call": LOG.info, "count": randint(1, 10), "msg": "This is an info log", "level": "INFO"},
        {"call": LOG.warning, "count": randint(1, 10), "msg": "This is a warning log",
         "level": "WARNING"},
        {"call": LOG.error, "count": randint(1, 10), "msg": "This is an error log",
         "level": "ERROR"},
        {
            "call": LOG.critical,
            "count": randint(1, 10),
            "msg": "This is a critical log",
            "level": "CRITICAL",
        },
    ]
    for call in calls:
        if call.get("level") == "DEBUG":
            continue
        for _ in range(call["count"]):
            call["call"](call["msg"])
        assert COUNTING_HANDLER.counts[call["level"]] == call["count"]
    LOG.info(COUNTING_HANDLER.counts)


def test_console_debug_log():
    LOG.debug("DEBUG = %s", COUNTING_HANDLER.counts["DEBUG"])


def test_console_info_log():
    LOG.info("INFO = %s", COUNTING_HANDLER.counts["INFO"])


def test_console_warning_log():
    LOG.warning("WARNING = %s", COUNTING_HANDLER.counts["WARNING"])


def test_console_error_log():
    LOG.error("ERROR = %s", COUNTING_HANDLER.counts["ERROR"])


def test_console_critical_log():
    LOG.critical("CRITICAL = %s", COUNTING_HANDLER.counts["CRITICAL"])
