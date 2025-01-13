import logging
from logging.handlers import SysLogHandler

import socket
import pytest
from src.ibx_sdk.logger.ibx_logger import init_remote_logger
from syslog_rfc5424_formatter import RFC5424Formatter


def test_init_remote_logger_default_values():
    logger = init_remote_logger(
        address=("192.168.1.53", 5140),
        level="DEBUG"
    )
    logger.debug("Test DEBUG message")
    logger.info("Test INFO message")
    logger.warning("Test WARNING message")
    logger.error("Test ERROR message")
    logger.critical("Test CRITICAL message")

    handlers = logger.handlers
    # assert len(handlers) > 0
    handler = handlers[0]
    # assert isinstance(handler, SysLogHandler)
    # assert handler.address == ("192.168.1.53", 5140)
    # assert handler.facility == SysLogHandler.facility_names["local0"]
    # assert handler.socktype == logging.handlers.SOCK_STREAM
    # assert isinstance(handler.formatter, RFC5424Formatter)


# @pytest.mark.parametrize(
#     "level, expected_level",
#     [("DEBUG", logging.DEBUG), ("INFO", logging.INFO), ("WARNING", logging.WARNING)],
# )
# def test_init_remote_logger_log_level(level, expected_level):
#     logger = init_remote_logger(level=level)
#     assert logger.level == expected_level
#
#
# @pytest.mark.parametrize("protocol, socktype",
#                          [("TCP", socket.SOCK_STREAM), ("UDP", socket.SOCK_DGRAM)])
# def test_init_remote_logger_protocol(protocol, socktype):
#     logger = init_remote_logger(protocol=protocol)
#     handler = logger.handlers[0]
#     assert handler.socktype == socktype
#
#
# def test_init_remote_logger_custom_address_and_facility():
#     logger = init_remote_logger(address=("custom_host", 1514), facility="daemon")
#     handler = logger.handlers[0]
#     assert handler.address == ("custom_host", 1514)
#     assert handler.facility == SysLogHandler.facility_names["daemon"]
