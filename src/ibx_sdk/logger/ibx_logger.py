"""
Copyright 2023 Infoblox

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging
import os
import socket
from collections import Counter
from logging.handlers import RotatingFileHandler
from typing import Optional

import coloredlogs
from syslog_rfc5424_formatter import RFC5424Formatter


class CountingHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.counts = Counter()

    def emit(self, record: logging.LogRecord) -> None:
        self.counts[record.levelname] += 1


log_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def init_logger(
    logfile_name: str,
    logfile_mode: Optional[str] = "w",
    console_log: Optional[bool] = None,
    log_format: Optional[str] = None,
    max_size: Optional[int] = None,
    num_logs: Optional[int] = None,
    level: Optional[str] = None,
) -> logging.Logger:
    """
    Create and return a custom file/console logger.

    Args:
        logfile_name (str): The name of the log file.
        logfile_mode (str, optional): Specify the mode for the log file. 'a' for
            append or 'w' for write mode for basic file logging.
        console_log (bool, optional): If True, create a colored console log.
        log_format (str, optional): Specify the format for the log messages.
        max_size (int, optional): Specify the maximum size for the log file (in
            bytes) if you want to use a rotating log file handler instead of a
            standard log file handler.
        num_logs (int, optional): Specify the number of log files to keep if you
            want to use a rotating log file handler instead of a standard log
            file handler.
        level (str, optional): Specify a string value for the logging level. This
            field is case-insensitive and will default to 'INFO' if not provided.

    Returns:
        logging.Logger: The root logger.

    Example:

    **Basic FileHandler**
    ```python
    from ibx_sdk.logger.ibx_logger import init_logger

    # Initialize a basic logger to a file using write mode
    log = init_logger('logs/mylog.log', 'w')
    ```

    **Advanced RotatingFileHandler**
    ```python
    from ibx_sdk.logger.ibx_logger import init_logger

    # Initialize rotating file logging

    log = init_logger(
        logfile_name='logs/mylog.log',
        max_size=1000000,
        num_logs=10
    )
    ```
    """
    if level:
        log_level = log_levels.get(level.upper(), logging.INFO)
    else:
        log_level = logging.INFO

    if log_format:
        log_fmt = log_format
    else:
        log_fmt = (
            "%(asctime)s [%(filename)s:%(lineno)d - %(funcName)s()] %(levelname)s %(message)s"
        )

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # feature - logfile path
    if os.getenv("IBX_LOGDIR"):
        if not os.path.exists(os.getenv("IBX_LOGDIR")):
            try:
                os.makedirs(os.getenv("IBX_LOGDIR"))
            except FileExistsError as err:
                logging.warning(err)
            except OSError as err:
                logging.warning(err)
        logfile_name = os.path.join(os.getenv("IBX_LOGDIR"), logfile_name)

    if num_logs and max_size:
        lfh = RotatingFileHandler(
            filename=logfile_name, maxBytes=max_size, backupCount=num_logs
        )
    else:
        lfh = logging.FileHandler(
            filename=logfile_name,
            mode=logfile_mode,
        )
    lfh.setFormatter(logging.Formatter(log_fmt))
    lfh.setLevel(log_level)
    root_logger.addHandler(lfh)

    if console_log:
        init_console_logger(level, log_format)

    root_logger.debug("using logfile_name = %s", logfile_name)
    return root_logger


def init_remote_logger(
    address: tuple[str, int] = ("localhost", 5140),
    facility: str = "local0",
    protocol: str = "TCP",
    level: Optional[str] = None,
) -> logging.Logger:
    if level:
        log_level = log_levels.get(level.upper())
    else:
        log_level = logging.INFO
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    socktype = socket.SOCK_STREAM if protocol == "TCP" else socket.SOCK_DGRAM
    handler = logging.handlers.SysLogHandler(
        address=address, facility=facility, socktype=socktype
    )
    handler.append_nul = False
    handler.setFormatter(RFC5424Formatter())
    root_logger.addHandler(handler)
    current_fmt = handler.formatter._fmt
    new_fmt = logging.Formatter(current_fmt + "\n")
    handler.setFormatter(new_fmt)
    return root_logger


def init_console_logger(
    level: Optional[str] = None, log_format: Optional[str] = None
):
    """
    Initialize a colored console logger with optional custom logging level.

    Args:
        level (str, optional): Specify a string value of the logging level.
            This field is case-insensitive and will default to 'INFO' if not provided.
        log_format (str, optional): Specify the format for the log messages.
            This field has a default value.


    Example:

    **Initialize Colored console logger with a custom logging level**
    ```python
    from ibx_sdk.logger.ibx_logger import init_console_logger

    # Initialize a console logger with a custom logging level
    init_console_logger(level='DEBUG')
    ```

    """
    if level:
        log_level = log_levels.get(level.upper(), logging.INFO)
    else:
        log_level = logging.INFO
    coloredlogs.DEFAULT_FIELD_STYLES["filename"] = dict(color="blue")

    if log_format:
        log_fmt = log_format
    else:
        log_fmt = (
            "%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s %(message)s"
        )
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    coloredlogs.install(logger=root_logger, level=log_level, fmt=log_fmt)
    return root_logger


def increase_log_level(handler_type: str = "both") -> None:
    """
    Increase the logging level of the root logger and specific handlers.

    Args:
        handler_type (str, optional): Specify the type of handlers to increase
            the logging level for. Can be 'both' (default), 'console', or 'file'.

    Returns:
        None

    Example:

    **Increase Log Level**
    ```python
    from your_module import increase_log_level

    # Increase the logging level for both console and file handlers
    increase_log_level()

    # Increase the logging level for console handlers only - use 'both' to increase the file and
    # console handlers
    increase_log_level(handler_type='console')
    ```
    """

    defined_levels = sorted(set(_defined_levels().values()))
    root_logger = logging.getLogger()
    current_level = root_logger.getEffectiveLevel()
    current_index = defined_levels.index(current_level)
    selected_index = max(0, current_index - 1)
    root_logger.setLevel(defined_levels[selected_index])
    for handle in root_logger.handlers:
        if isinstance(
            handle, coloredlogs.StandardErrorHandler
        ) and handler_type in [
            "both",
            "console",
        ]:
            current_index = defined_levels.index(handle.level)
            selected_index = max(0, current_index - 1)
            coloredlogs.set_level(defined_levels[selected_index])
        elif (
            isinstance(handle, logging.FileHandler)
            or isinstance(handle, logging.handlers.RotatingFileHandler)
            and handler_type in ["both", "file"]
        ):
            current_index = defined_levels.index(handle.level)
            selected_index = max(0, current_index - 1)
            handle.setLevel(defined_levels[selected_index])


def set_log_level(level: str, handler_type: str = "both") -> None:
    """
    Set the logging level for the root logger and specific handlers.

    Args:
        level (str): The desired logging level, e.g., 'DEBUG', 'INFO', 'WARNING'.
            This field is case-insensitive.
        handler_type (str, optional): Specify the type of handlers to set the
            logging level for. Can be 'both' (default), 'console', or 'file'.

    Returns:
        None

    Example:

    **Set the logging level for both console and file handlers to 'DEBUG'**

    ```python
    from your_module import set_log_level

    # Set the logging level for both console and file handlers
    set_log_level(level='DEBUG')

    # or more explicitly using:
    set_log_level(level='DEBUG', handler_type='both')

    # Set the logging level for console handlers only to 'INFO'
    set_log_level(level='INFO', handler_type='console')
    ```

    """
    log_level = log_levels.get(level.upper(), logging.INFO)
    root_logger = logging.getLogger()
    if handler_type == "both":
        root_logger.setLevel(log_level)
    for handle in root_logger.handlers:
        if isinstance(
            handle, coloredlogs.StandardErrorHandler
        ) and handler_type in [
            "both",
            "console",
        ]:
            coloredlogs.set_level(log_level)
        elif (
            isinstance(handle, logging.FileHandler)
            or isinstance(handle, logging.handlers.RotatingFileHandler)
            and handler_type in ["both", "file"]
        ):
            handle.setLevel(log_level)


def _defined_levels():
    defined_levels = {}
    for name in dir(logging):
        if name.isupper():
            value = getattr(logging, name)
            if isinstance(value, int):
                defined_levels[name] = value
    return defined_levels
