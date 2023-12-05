# pylint: disable-msg=too-many-arguments
"""
custom logging module
"""
import os
from typing import Optional
from logging.handlers import RotatingFileHandler
import logging
import coloredlogs

log_levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


class CallCounted:
    """Decorator to determine the # of calls for a method"""

    def __init__(self, method):
        self.method = method
        self.counter = 0

    def __call__(self, *args, **kwargs):
        self.counter += 1
        return self.method(*args, **kwargs)


def init_logger(
        logfile_name: str,
        logfile_mode: Optional[str] = 'w',
        console_log: Optional[bool] = None,
        max_size: Optional[int] = None,
        num_logs: Optional[int] = None,
        level: Optional[str] = None) -> logging.Logger:
    """
    create and return custom file/console logger

    :param logfile_name: log file name
    :param logfile_mode: (optional) specify this value to set the logging file
        mode 'a' for append or 'w' for write mode for basic file logging
    :param console_log: if true, create a colored console log
    :param max_size: (optional) specify a logfile size if you would like to
        use a rotating log file handler vs standard log file handler
    :param num_logs: (optional) specify a logfile count if you would like
        to use a rotating log file handler vs standard log file handler
    :param level: (optional) specify a string value of logging level. This field
        is case-insensitive and will default to logging.INFO

    :return: return root logger

    Example::

    **Basic FileHandler**

        from infoblox_pslib.util.ibx_logger import init_logger

        # initialize basic logger to file using write mode
        log = init_logger('logs/mylog.log', 'w')

    **Advanced RotatingFileHandler**

        from infoblox_pslib.util.ibx_logger import init_logger

        # initialize rotating file logging
        log = init_logger(
            logfile_name='logs/mylog.log',
            logfile_size=1000000,
            logfile_count=10
        )

    """
    if level:
        log_level = log_levels.get(level.upper(), logging.INFO)
    else:
        log_level = logging.INFO
    log_fmt = '%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s %(message)s'
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # feature - logfile path
    if os.getenv('IBX_LOGDIR'):
        if not os.path.exists(os.getenv('IBX_LOGDIR')):
            try:
                os.makedirs(os.getenv('IBX_LOGDIR'))
            except FileExistsError as err:
                logging.warning(err)
            except OSError as err:
                logging.warning(err)
        logfile_name = os.path.join(os.getenv('IBX_LOGDIR'), logfile_name)

    if num_logs and max_size:
        lfh = RotatingFileHandler(
            filename=logfile_name,
            maxBytes=max_size,
            backupCount=num_logs
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
        init_console_logger(level)

    root_logger.debug('using logfile_name = %s', logfile_name)
    return root_logger


def init_console_logger(level: Optional[str] = None):
    """
    Initialize a colored console logger

    :param level: (optional) specify string value of logging level. This field
        is case-insensitive and will default to logging.INFO otherwise.
    """
    if level:
        log_level = log_levels.get(level.upper(), logging.INFO)
    else:
        log_level = logging.INFO
    coloredlogs.DEFAULT_FIELD_STYLES['filename'] = dict(color='blue')
    log_fmt = '%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s %(message)s'
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    coloredlogs.install(
        logger=root_logger,
        level=log_level,
        fmt=log_fmt
    )


def increase_log_level(handler_type: str = 'both') -> None:
    """
    increase logging level to DEBUG

    :param handler_type: specify the type of handler 'both' (default), 'file' or 'console'

    :return None:
    """
    defined_levels = sorted(set(_defined_levels().values()))
    root_logger = logging.getLogger()
    current_level = root_logger.getEffectiveLevel()
    current_index = defined_levels.index(current_level)
    selected_index = max(0, current_index - 1)
    root_logger.setLevel(defined_levels[selected_index])
    for handle in root_logger.handlers:
        if (
                isinstance(handle, coloredlogs.StandardErrorHandler) and
                handler_type in ['both', 'console']
        ):
            current_index = defined_levels.index(handle.level)
            selected_index = max(0, current_index - 1)
            coloredlogs.set_level(defined_levels[selected_index])
        elif (
                isinstance(handle, logging.FileHandler) or
                isinstance(handle, logging.handlers.RotatingFileHandler) and
                handler_type in ['both', 'file']
        ):
            current_index = defined_levels.index(handle.level)
            selected_index = max(0, current_index - 1)
            handle.setLevel(defined_levels[selected_index])


def set_log_level(level: str, handler_type: str = 'both') -> None:
    """
    set logging level

    :param level: specify string value of logging level. This field
        is case-insensitive and will default to logging.INFO otherwise.
    :param handler_type: specify the type of handler 'file' or 'console' or 'both'
        defaults to 'both'
    """
    log_level = log_levels.get(level.upper(), logging.INFO)
    root_logger = logging.getLogger()
    if handler_type == 'both':
        root_logger.setLevel(log_level)
    for handle in root_logger.handlers:
        if (
                isinstance(handle, coloredlogs.StandardErrorHandler) and
                handler_type in ['both', 'console']
        ):
            coloredlogs.set_level(log_level)
        elif (
                isinstance(handle, logging.FileHandler) or
                isinstance(handle, logging.handlers.RotatingFileHandler) and
                handler_type in ['both', 'file']
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
